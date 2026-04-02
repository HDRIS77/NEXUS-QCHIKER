from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
# تفعيل CORS للسماح للإضافة بالاتصال بالسيرفر من أي مكان
CORS(app, resources={r"/api/*": {"origins": "*"}})

GEMINI_API_KEY = "AIzaSyD57uIR2ncdeYRXPubooxXo-xJzfKbLE-o"

@app.route('/')
def home():
    return "NEXUS-QCHIKER API is Running."

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
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

        # الـ Prompt الدقيق لاستخراج البيانات بالمنطق الذي شرحته
        prompt_text = """
        Analyze these Salesforce screenshots. Return ONLY a JSON object with:
        1. nineCookieId: numeric ID from Backend ID.
        2. city: From Address (Restaurant type).
        3. francoName: Arabic transliteration of the branch name.
        4. vat: percentage value.
        5. creditCard: boolean (true if Credit Card Payment Fee exists).
        6. deliveryType: 'TGO' if OD/Talabat TGO, 'TMP' if MP/Vendor Delivery.
        7. gridAlert: 'تنبيه: يوجد GRID' if GRID found outside Account Name.
        8. vatNotice: 'يرجى التأكد من تفعيل الـ VAT في باقي الفروع' if Egypt.
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}] + image_parts
            }]
        }

        response = requests.post(url, json=payload, timeout=30)
        res_json = response.json()

        # استخراج النص وتنظيفه من أي Markdown
        raw_text = res_json['candidates'][0]['content']['parts'][0]['text']
        clean_json = raw_text.replace("```json", "").replace("```", "").strip()
        
        return jsonify(json.loads(clean_json))

    except Exception as e:
        return jsonify({"error": str(e)}), 500
