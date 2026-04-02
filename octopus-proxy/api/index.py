from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
# ده السطر اللي بيسمح للكروم إكستنشن تكلم السيرفر بدون قيود
CORS(app, resources={r"/api/*": {"origins": "*"}})

GEMINI_API_KEY = "AIzaSyD57uIR2ncdeYRXPubooxXo-xJzfKbLE-o"

@app.route('/')
def home():
    return "NEXUS API is Active"

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    # معالجة طلب الـ Preflight اللي بيبعته الكروم للتأكد من الأمان
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json()
        if not data or 'images' not in data:
            return jsonify({"error": "No images provided"}), 400

        image_parts = []
        for img in data['images']:
            image_parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": img
                }
            })

        # الـ Prompt الاحترافي اللي اتفقنا عليه
        prompt_text = "Analyze these Salesforce screenshots. Extract: Backend ID, City/Area (Restaurant type only), Name (Franco logic), Delivery Type (OD/TGO vs MP/TMP), Payment methods, and VAT. Alert if GRID is found outside Account Name."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}] + image_parts
            }]
        }

        response = requests.post(url, json=payload, timeout=30)
        res_json = response.json()

        # تنظيف الرد من الـ Markdown لضمان وصول JSON صافي للإضافة
        raw_text = res_json['candidates'][0]['content']['parts'][0]['text']
        clean_json = raw_text.replace("```json", "").replace("```", "").strip()
        
        return jsonify(json.loads(clean_json))

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
