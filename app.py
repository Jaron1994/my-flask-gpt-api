from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import io
from pdfminer.high_level import extract_text

app = Flask(__name__)
CORS(app)

# Load OpenAI API Key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Welcome to the Resume Analyzer API! 🎉"

# 🔹 Endpoint to analyze resume
@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        # Get the uploaded file and job title
        file = request.files['resume']
        job_title = request.form.get('job_title', '')

        # Ensure a file was uploaded
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Convert PDF to text
        resume_text = extract_text(io.BytesIO(file.read()))

        # Send resume text and job title to OpenAI
        prompt = f"Analyze the following resume and give feedback based on the target job title: {job_title}\n\nResume:\n{resume_text}"
        
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify({"response": response["choices"][0]["message"]["content"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
