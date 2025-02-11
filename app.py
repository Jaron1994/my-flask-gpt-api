from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from pdfminer.high_level import extract_text
import os

app = Flask(__name__)
CORS(app)

# Load OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Resume Analyzer API is running!"

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    if "resume" not in request.files or "job_title" not in request.form:
        return jsonify({"error": "Missing resume file or job title"}), 400

    resume_file = request.files["resume"]
    job_title = request.form["job_title"]

    # Extract text from PDF
    try:
        resume_text = extract_text(resume_file)
    except Exception as e:
        return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 500

    # Send to OpenAI for analysis
    prompt = f"Analyze this resume for the job title '{job_title}' and provide feedback:\n\n{resume_text}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        feedback = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return jsonify({"error": f"OpenAI API request failed: {str(e)}"}), 500

    return jsonify({"feedback": feedback})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
