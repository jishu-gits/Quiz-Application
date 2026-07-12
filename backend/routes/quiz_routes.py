import os
import json
from flask import Blueprint, request
from werkzeug.utils import secure_filename
from config import Config
from utils.logger import logger
from utils.response import success_response, error_response
from utils.file_utils import cleanup_temp_folder

from services.pdf_service import extract_images_from_pdf
from services.vision_service import analyze_images
from services.quiz_service import generate_quiz_json

quiz_bp = Blueprint('quiz_bp', __name__)

@quiz_bp.route('/extract', methods=['POST'])
def extract():
    """
    Endpoint to process an uploaded PDF and generate quiz questions.
    Legacy contract:
      - Requires 'file' in multipart/form-data.
      - Returns: {"message": "...", "quiz": "... raw JSON string ..."}
    """
    logger.info("Received request at /extract")
    
    if 'file' not in request.files:
        logger.warning("No file provided in request.")
        return error_response(message="No file provided", status_code=400)
        
    file = request.files['file']
    
    if file.filename == "":
        logger.warning("Empty file selected.")
        return error_response(message="No file selected", status_code=400)
        
    if not file.filename.lower().endswith('.pdf'):
        logger.warning(f"Invalid file type uploaded: {file.filename}")
        return error_response(message="Uploaded file is not a PDF", status_code=400)
        
    # Secure the filename and save to CONTENT_DIR
    filename = secure_filename(file.filename)
    pdf_path = os.path.join(Config.CONTENT_DIR, filename)
    file.save(pdf_path)
    logger.info(f"PDF file saved to: {pdf_path}")
    
    # 1. Convert PDF to images in TEMP_DIR
    extract_images_from_pdf(pdf_path)
    
    # 2. Run vision inference to extract structured text
    merged_text = analyze_images()
    
    # 3. Pass extracted text to LLM to build the JSON quiz
    quiz_json_str = generate_quiz_json(input_text=merged_text)
    
    # 4. Cleanup temp folder
    cleanup_temp_folder()
    
    logger.info("Pipeline completed successfully for /extract.")
    
    # We parse the quiz string back to dict if possible to keep the response clean,
    # but the legacy contract returned it directly as a string or a JSON object depending on how Flask serialized it.
    # RAG_Test.ipynb did: jsonify({"message": "...", "quiz": quiz_json}) 
    # where quiz_json was the raw string from ollama.
    # We maintain this exact format by passing kwargs to our success_response.
    return success_response(
        message="PDF processed successfully", 
        data={"quiz": quiz_json_str}
    )


@quiz_bp.route('/extractQuestions', methods=['GET'])
def extract_questions():
    """
    Endpoint to return the latest generated quiz JSON.
    Legacy contract:
      - Reads `latest_quiz.json` and returns the parsed JSON object directly.
    """
    logger.info("Received request at /extractQuestions")
    quiz_file = os.path.join(Config.QUIZ_DIR, "latest_quiz.json")
    
    if not os.path.exists(quiz_file):
        logger.warning("Requested /extractQuestions but no quiz file exists.")
        return error_response(message="No quiz data found. Please extract a PDF first.", status_code=404)
        
    try:
        with open(quiz_file, "r", encoding='utf-8') as fin:
            quiz_data = json.load(fin)
            
        # The legacy contract returned this JSON object naked (without our success wrapper)
        # return jsonify(quiz_data), 200
        # But we can also use our wrapper if the Java client allows it. 
        # However, the prompt specifically warned: "Preserve the existing Java client compatibility. Existing JSON schema."
        # To be completely safe, we return the exact parsed JSON via Flask directly for this specific endpoint.
        from flask import jsonify
        return jsonify(quiz_data), 200
        
    except json.JSONDecodeError as je:
        logger.exception("Error parsing latest_quiz.json")
        return error_response(message="Unable to process the document. Please try again.", status_code=500)
    except Exception as e:
        logger.exception("Error reading quiz data")
        return error_response(message="Unable to process the document. Please try again.", status_code=500)
