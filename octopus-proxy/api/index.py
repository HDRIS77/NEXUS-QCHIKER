from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# ضع مفتاح Gemini الخاص بك هنا
GEMINI_API_KEY = "AIzaSyD57uIR2ncdeYRXPubooxXo-xJzfKbLE-o"

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        base64_image = data.get("image")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        # الـ Prompt الموجه لاستخراج بيانات طلبات بدقة
        prompt = "Extract data from this Talabat/Sufra screenshot. Return ONLY a JSON object with keys: city, areaEn, areaAr, nineCookieId. Format: {\"city\": \"...\", \"areaEn\": \"...\", \"areaAr\": \"...\", \"nineCookieId\": \"...\"}"
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": base64_image}}
                ]
            }]
        }
        
        response = requests.post(url, json=payload)
        response_data = response.json()
        
        # استخراج النص من رد جيميناي وتنظيفه
        raw_text = response_data['candidates'][0]['content']['parts'][0]['text']
        clean_json = raw_text.replace("```json", "").replace("```", "").strip()
        
        return jsonify(json.loads(clean_json))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# لضمان عمله على Vercel
def handler(event, context):
    return app(event, context)