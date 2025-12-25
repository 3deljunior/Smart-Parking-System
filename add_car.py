# add_car.py
import requests
import json

url = "http://127.0.0.1:8000/add_car"

# مثال: عربية جديدة
data = {
    "owner_name": "وفة",
    "car_type": "koda",
    "color": "black",
    "plate_no": "خ ي ث",
    "category": "prvate"
}

try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # هيرمي استثناء لو حصل خطأ
    print("تمت العملية بنجاح، الرد من السيرفر:")
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    try:
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except:
        print("خطأ في قراءة الرد من السيرفر")
except Exception as err:
    print(f"Other error occurred: {err}")
