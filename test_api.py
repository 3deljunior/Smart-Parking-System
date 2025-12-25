#test_api.py
import requests
import json

url = "http://127.0.0.1:8000/add_car"

data = {
    "owner_name": "Ahmed",
    "car_type": "BMW",
    "color": "Black",
    "plate_no": " ١ ٢ ٣ ٤ س م ن",
    "category": "VIP"
}

# إرسال بيانات العربية للـ API
r = requests.post(url, json=data)

# عرض الرد بشكل JSON مرتب ومباشر بالعربي
print(json.dumps(r.json(), ensure_ascii=False, indent=2))
