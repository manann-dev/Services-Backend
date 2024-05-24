from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Api, Resource, Namespace, fields
from werkzeug.datastructures import FileStorage
import io
import json

from openai import OpenAI
from config import client, CONFIG_FILE

# Define the namespace
training_ns = Namespace('training', description='Training operations')

# Define the file upload parser
upload_parser = training_ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='The file to upload for training')


# Upload File Endpoint
@training_ns.route('/uploadFile')
class UploadFile(Resource):
    @jwt_required()
    @training_ns.doc(security='Bearer Auth')
    @training_ns.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is the file object received from the request

        if uploaded_file:
            try:
                # Read the file content into a bytes-like object
                file_content = uploaded_file.read()
                
                # Create an in-memory file-like object from bytes
                in_memory_file = io.BytesIO(file_content)
                
                # Attempt to upload the file-like object
                response = client.files.create(
                    file=in_memory_file,
                    purpose="fine-tune"
                )
                
                return json.loads(response.json()), 200
            except Exception as e:
                return {"error": str(e)}, 500


# Update the model to include optional hyperparameters
training_model = training_ns.model('StartTrainModel', {
    'model': fields.String(required=True, description='The model to train'),
    'training_file_id': fields.String(required=True, description='The training file ID'),
    # Optional fields
    'n_epochs': fields.Integer(required=False, description='Number of training epochs', default=2),  # Default value as an example
    'validation_file_id': fields.String(required=False, description='The validation file ID')
})

@training_ns.route('/startTrain')
class StartTrain(Resource):
    @jwt_required()
    @training_ns.doc(security='Bearer Auth')
    @training_ns.doc('start_train')
    @training_ns.expect(training_model)
    def post(self):
        data = request.json
        model = data['model']
        training_file_id = data['training_file_id']
        # Extract optional parameters, with defaults if not provided
        n_epochs = data.get('n_epochs', 3)  # Default to 4 epochs if not specified
        validation_file_id = data.get('validation_file_id', None)  # None if not provided

        try:
            # Pass optional parameters to the fine-tuning job creation method
            response = client.fine_tuning.jobs.create(
                training_file=training_file_id, 
                model=model,
                hyperparameters = {
                    "n_epochs": n_epochs
                },
                validation_file=validation_file_id  # Pass None if no validation file is specified
            )
            return json.loads(response.json()), 200
        except Exception as e:
            return {"error": str(e)}, 500

# List Jobs Endpoint
@training_ns.route('/listJobs')
class ListJobs(Resource):
    @training_ns.doc(security='Bearer Auth')
    @jwt_required()
    @training_ns.doc('list_jobs')
    def get(self):
        try:
            jobs = client.fine_tuning.jobs.list(limit=10)
            
            return json.loads(jobs.json()), 200
        except Exception as e:
            return {"error": str(e)}, 500

# Retrieve Job Endpoint
@training_ns.route('/retrieveJob/<job_id>')
class RetrieveJob(Resource):
    @jwt_required()
    @training_ns.doc(security='Bearer Auth')
    @training_ns.doc('retrieve_job')
    def get(self, job_id):
        try:
            job = client.fine_tuning.jobs.retrieve(job_id)
            return json.loads(job.json()), 200
        except Exception as e:
            return {"error": str(e)}, 500
        
# Cancel Job Endpoint
@training_ns.route('/cancelJob/<job_id>')
class CancelJob(Resource):
    @jwt_required()
    @training_ns.doc(security='Bearer Auth')
    @training_ns.doc('cancel_job')
    def post(self, job_id):
        try:
            job = client.fine_tuning.jobs.cancel(job_id)
            return {"message": "Job canceled successfully", "job": json.loads(job.json())}, 200
        except Exception as e:
            return {"error": str(e)}, 500

# List Job Events Endpoint
@training_ns.route('/listJobEvents/<fine_tuning_job_id>')
class ListJobEvents(Resource):
    @jwt_required()
    @training_ns.doc(security='Bearer Auth')
    @training_ns.doc('list_job_events')
    def get(self, fine_tuning_job_id):
        try:
            events = client.fine_tuning.jobs.list_events(fine_tuning_job_id=fine_tuning_job_id, limit=10)
            return json.loads(events.json()), 200
        except Exception as e:
            return {"error": str(e)}, 500

# Delete Model Endpoint
@training_ns.route('/deleteModel/<model_id>')
class DeleteModel(Resource):
    @jwt_required()
    @training_ns.doc(security='Bearer Auth')
    @training_ns.doc('delete_model')
    def delete(self, model_id):
        try:
            response = client.models.delete(model_id)
            return {"message": "Model deleted successfully", "model_id": model_id}, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
