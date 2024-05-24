from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import jwt_required
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import base64
from producer import celery

IMAGES_ENABLED = False # changes whether we ask chatgpt to describe images

# Create the namespace
pdf_parse_ns = Namespace('pdf_parse', description='PDF Parsing operations')

# Define the file upload parser for PDF parsing
pdf_upload_parser = pdf_parse_ns.parser()
pdf_upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='The PDF file to upload')


# Ask questions about PDF
@pdf_parse_ns.route('/askQuestionsAboutPDF/<model_name>')
@pdf_parse_ns.param('model_name', 'The model name to use for generating questions')
class AskQuestionsAboutPDF(Resource):
    @jwt_required()
    @pdf_parse_ns.doc(security='Bearer Auth')
    @pdf_parse_ns.expect(pdf_upload_parser)
    def post(self, model_name):
        args = pdf_upload_parser.parse_args()
        file = args['file']

        content_list = extract_content(file)
        # Generate background information
        tasks_ids = []
        
        for single_content in content_list:
            content_task = celery.send_task('tasks.ask_questions', args=[model_name, single_content, IMAGES_ENABLED])
            tasks_ids.append(content_task.id)
        
        # answers = chatGPTAsk.ask_questions(model_name, content_list, IMAGES_ENABLED)
        
        return {"tasks": tasks_ids}
    

    
# Parse PDF content
@pdf_parse_ns.route('/parsePDF')
class ParsePDF(Resource):
    @jwt_required()
    @pdf_parse_ns.doc(security='Bearer Auth')
    @pdf_parse_ns.expect(pdf_upload_parser)
    def post(self):
        args = pdf_upload_parser.parse_args()
        file = args['file']
        content_list = extract_content(file)

        # Generate background information
        tasks_ids = []
        
        for single_content in content_list:
            content_task = celery.send_task('tasks.generate_background_info', args=[single_content])
            tasks_ids.append(content_task.id)
        # background_information = chatGPTAsk.generate_background_info(content_list, images_enabled=False)
        
        return {"tasks": tasks_ids}

    
# Extracts content from the PDF
def extract_content(file_stream):
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    content_list = []  # Store extracted content

    for page_num, page in enumerate(doc):
        # Extract text
        text = page.get_text("text")
        content_list.append({'type': 'text', 'page': page_num, 'data': text})

        # Extract images and perform OCR
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)

            # Convert the image data to a PIL Image
            image_bytes = io.BytesIO(base_image["image"])
            pil_image = Image.open(image_bytes)

            # Use pytesseract to perform OCR on the image
            ocr_text = pytesseract.image_to_string(pil_image)

            # Only add OCR text if it's not empty
            if ocr_text.strip():
                content_list.append({'type': 'ocr_text', 'page': page_num, 'xref': xref, 'data': ocr_text.strip()})

            # Optionally, encode the image data as base64 and include it in the content list
            image_data = base64.b64encode(base_image["image"]).decode("utf-8")
            content_list.append({'type': 'image', 'page': page_num, 'xref': xref, 'image_data': image_data, 'img_index': img_index})

    doc.close()
    return content_list



