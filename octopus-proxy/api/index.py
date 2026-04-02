from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# ضع مفتاح Groq الخاص بك هنا
GROQ_API_KEY = "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"

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'images' not in data:
            return jsonify({"error": "No images"}), 400

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Return ONLY JSON: nineCookieId (numeric), city, francoName, vat (numeric), creditCard (boolean)."},
                *[{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}} for img in data['images']]
            ]
        }]

        payload = {
            "model": "llama-3.2-11b-vision-preview",
            "messages": messages,
            "response_format": {"type": "json_object"}
        }

        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()
        return jsonify(json.loads(res_data['choices'][0]['message']['content']))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
