import logging
import os
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from pdfminer.high_level import extract_text
from pdf2image import convert_from_bytes
import pytesseract

# Set Tesseract path for Render Free Tier
tesseract_path = os.path.expanduser("~/tesseract/bin/tesseract")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Resume Analyzer API is running!"

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        logging.info("Received request at /analyze")

        # Get uploaded file & job title
        file = request.files.get('resume')
        job_title = request.form.get('job_title', '')

        if not file:
            logging.error("No file uploaded")
            return jsonify({"error": "No file uploaded"}), 400

        logging.info(f"Received resume for job title: {job_title}")

        # Convert PDF file content into text
        resume_bytes = file.read()
        resume_text = extract_text(io.BytesIO(resume_bytes))

        if not resume_text.strip():  # If text extraction fails, try OCR
            logging.warning("Text extraction failed. Trying OCR...")
            images = convert_from_bytes(resume_bytes)
            resume_text = " ".join([pytesseract.image_to_string(img) for img in images])

        if not resume_text.strip():  # If OCR also fails, return an error
            logging.error("Failed to extract text from PDF")
            return jsonify({"error": "Failed to extract text from the resume"}), 500

        logging.info("Successfully extracted resume text")

        # Create OpenAI prompt
        prompt = f"Analyze this resume for the job title: {job_title}\n\n{resume_text}"

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        logging.info("Successfully got response from OpenAI")

        return jsonify({"response": response["choices"][0]["message"]["content"]})

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
