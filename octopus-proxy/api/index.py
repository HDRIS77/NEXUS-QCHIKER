from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# حط هنا الـ API Key اللي طلعته من Google AI Studio
GEMINI_API_KEY = "AIzaSyD57uIR2ncdeYRXPubooxXo-xJzfKbLE-o"

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        base64_images = data.get("images") # استلام مصفوفة صور لو رفعت أكتر من واحدة
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        prompt = """
        Analyze the provided Salesforce/Talabat screenshots and extract data into a JSON object. Rules:
        1. Address: ONLY from 'Addresses' where type includes 'Restaurant'.
        2. Backend ID: Extract from 'Platforms Performance' or 'Backend ID'.
        3. Naming: If Arabic, extract text BEFORE right comma. If English, extract text BEFORE left comma and provide 'francoName' (transliteration).
        4. Delivery: 'OD'/'Talabat TGO' -> 'TGO'. 'MP'/'Self Delivery' -> 'TMP'.
        5. Payments: 'cash' is always true. 'creditCard' is true if 'Credit Card Payment Fee' exists.
        6. VAT: Extract % value. If Egypt, set 'vatNotice' to 'يرجى التأكد من تفعيل الـ VAT في باقي الفروع المرتبطة'.
        7. GRID Alert: Ignore GRID under Account Name. If GRID is found ANYWHERE else, set 'gridAlert' to 'تنبيه: يوجد GRID في هذه الصفحة'.
        8. Warning: If multiple VAT values found, set 'vatWarning' to '⚠️ تنبيه: يوجد قيم ضريبية مختلفة'.
        Return ONLY a clean JSON object.
        """
        
        # تجهيز الصور للإرسال لـ Gemini
        image_parts = [{"inline_data": {"mime_type": "image/jpeg", "data": img}} for img in base64_images]
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}] + image_parts
            }]
        }
        
        response = requests.post(url, json=payload)
        res_json = response.json()
        
        raw_text = res_json['candidates'][0]['content']['parts'][0]['text']
        clean_json = raw_text.replace("```json", "").replace("```", "").strip()
        
        return jsonify(json.loads(clean_json))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
