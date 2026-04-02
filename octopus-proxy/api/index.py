from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# حط مفتاح Groq هنا
GROQ_API_KEY = "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"

@app.route('/')
def home():
    return "NEXUS-QCHIKER Groq API is Running."

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json()
        if not data or 'images' not in data:
            return jsonify({"error": "No images provided"}), 400

        # بما أن Groq يفضل النصوص، سنستخدم Gemini كـ OCR (لو متاح) 
        # أو نرسل الصور لموديل Llama-3-2-Vision على Groq (لو متاح في حسابك)
        # هنا سنستخدم الموديل البصري لـ Groq: llama-3.2-11b-vision-preview
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        # تجهيز الصور لـ Groq (بصيغة مشابهة لـ OpenAI)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract from these Salesforce screenshots: nineCookieId (Backend ID), City (Restaurant address), Franco branch name, VAT %, and payment methods. Return ONLY JSON."},
                    *[
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img}"}
                        } for img in data['images']
                    ]
                ]
            }
        ]

        payload = {
            "model": "llama-3.2-11b-vision-preview", # موديل الرؤية في Groq
            "messages": messages,
            "response_format": {"type": "json_object"} # يضمن رجوع JSON
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        res_json = response.json()
        
        # استخراج النتيجة
        content = res_json['choices'][0]['message']['content']
        return jsonify(json.loads(content))

    except Exception as e:
        return jsonify({"error": str(e)}), 500
