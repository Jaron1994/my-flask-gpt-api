from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Load OpenAI API Key from Environment Variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🔹 Add a Homepage Route to Prevent 404 Errors
@app.route('/')
def home():
    return "Welcome to My Flask GPT API! 🎉 Your service is running."

# 🔹 Your Chatbot API Route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "")

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": user_input}]
    )

    return jsonify({"response": response["choices"][0]["message"]["content"]})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
