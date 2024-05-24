import os
from flask_restx import Api
from datetime import timedelta , datetime
from flask_sqlalchemy import SQLAlchemy
from pdfParse import pdf_parse_ns
from training import training_ns
from auth import auth_ns
from schema.models import user
from schema.models.user import User
from flask import Flask, request, jsonify , flash , url_for , redirect , render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

api = Api(app, version='1.0', title='API Documentation', description='An API wrapper for OpenAI.', security='Bearer Auth', authorizations=authorizations)

# Add namespaces instead of registering blueprints
api.add_namespace(pdf_parse_ns)
api.add_namespace(training_ns)
api.add_namespace(auth_ns)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['GOOGLE_CLIENT_ID'] = os.getenv("GOOGLE_CLIENT_ID")
app.config['GOOGLE_SECRET_KEY'] = os.getenv("GOOGLE_SECRET_KEY")
app.config['GOOGLE_REDIRECT_URI'] = os.getenv("GOOGLE_REDIRECT_URI")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message':'test route'}),200


@app.route('/create_user_by_admin', methods=['POST'])
def create_user_byAdmin():
    try:
        data = request.get_json()

        existing_user_by_email = user.query.filter_by(email=data['email']).first()

        if existing_user_by_email:
            return jsonify({'message': 'User Already Exists'})
        new_user = user(
            id = data['id'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email']
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message' : 'User Created!'}),200
    except Exception as e:
        return jsonify({'message' : 'Error creating user'}),500


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password = form.password.data,
            created_at=datetime.utcnow()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login')) 
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user1 = user.query.filter_by(email=data['email']).first()

        if user1 and user1.check_password(data['password']):
            access_token = create_access_token(identity=data['email'])
            return jsonify({'message': 'Login successful', 'accerss_token': access_token, 'id': user1.id}),200
        else:
            return jsonify({'message': 'Invalid email or password'}),401
    except Exception as e:
        return jsonify({'message': 'Error logging in'}),500


@app.route('/update_user/<id>', methods=['PUT'])
@jwt_required
def update_user(id):
    try:
        user1 = user.query.filter_by(id=id).first()
        if user1:
            data = request.get_json()
            user1.id = data['id']
            user1.first_name = data['first_name']
            user1.last_name = data['last_name']
            user1.email = data['email']
            user1.password = data['password']
            db.session.commit()
            return jsonify({'message': 'User updated'}),200
        else:
            return jsonify({'message': 'User Not Found!'}),404
    except Exception as e:
        return jsonify({'message': 'Error updating user'}),500


@app.route('/delete_user/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user1 = user.query.filter_by(id=id).first()
        if user1:
            db.session.delete(user1)
            db.session.commit()
            return jsonify({'message':'User deleted!'}),200
        else:
            return jsonify({'message':'USer not found!'}),404
    except Exception as e:
        return jsonify({'message':'Error deleting user'}),500


@app.route('/get_users', methods=['GET'])
def get_users():
    user1 = user.query.all()
    return jsonify({userr1.json() for userr1 in user1}),200


@app.route('/get_single_user/<id>', methods=['GET'])
def get_single_user(id):
    try:
        user1 = user.query.filter_by(id=id).first()
        if user1:
            return jsonify(user1.json()),200
        else:
            return jsonify({'message':'User Not Found!'}),404
    except Exception as e:
        return jsonify({'message':'Error getting user'}),500
    
    
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


with app.app_context():
    db.create_all()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
