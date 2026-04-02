from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
# تفعيل CORS للسماح للإضافة بالاتصال بالسيرفر
CORS(app)

# استبدل هذا بمفتاح الـ API الخاص بك
GEMINI_API_KEY = "AIzaSyD57uIR2ncdeYRXPubooxXo-xJzfKbLE-o"

@app.route('/')
def home():
    return "NEXUS-QCHIKER API is Running. Use /api/analyze for POST requests."

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        if not data or 'images' not in data:
            return jsonify({"error": "No images provided"}), 400

        images = data['images']
        
        # تجهيز محتوى الرسالة لـ Gemini
        contents = [
            {
                "parts": [
                    {"text": "Extract Backend ID, Commission values, VAT, and City from these Salesforce screenshots. If 'GRID' is mentioned near the account name, flag it."},
                    *[{"inline_data": {"mime_type": "image/png", "data": img}} for img in images]
                ]
            }
        ]

        # إرسال البيانات لـ Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        response = requests.post(url, json={"contents": contents})
        result = response.json()

        # هنا بنفترض إننا بنرجع JSON منظم للإضافة (تحتاج لتعديل حسب رد Gemini الفعلي)
        # هذا مثال للرد المتوقع من السيرفر للإضافة
        extracted_data = {
            "nineCookieId": "799436", # مثال من صورك
            "city": "Cairo", # مثال من صورك
            "francoName": "Bin Al-Gharbawi",
            "vat": "14%",
            "creditCard": True,
            "gridAlert": "⚠️ Attention: GRID found in Salesforce!"
        }

        return jsonify(extracted_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# مهم جداً لـ Vercel
if __name__ == '__main__':
    app.run(debug=True)
