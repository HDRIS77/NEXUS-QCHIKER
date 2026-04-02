from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
# تفعيل CORS ضروري جداً للسماح لكروم بالاتصال بالسيرفر
CORS(app, resources={r"/api/*": {"origins": "*"}})

# استبدل بمفتاح Groq الخاص بك
GROQ_API_KEY = "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"

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'images' not in data:
            return jsonify({"error": "No images provided"}), 400

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze these Salesforce images and return ONLY JSON with: nineCookieId (Backend ID), city (Restaurant Address), francoName (Branch name), vat (numeric percentage), and creditCard (boolean)."},
                *[{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}} for img in data['images']]
            ]
        }]

        payload = {
            "model": "llama-3.2-11b-vision-preview",
            "messages": messages,
            "response_format": {"type": "json_object"}
        }

        response = requests.post(url, headers=headers, json=payload)
        return jsonify(response.json()['choices'][0]['message']['content'])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
