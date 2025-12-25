import requests
import json

API_URL = "http://127.0.0.1:8000/checkout"

def checkout_car(plate_no):
    payload = {
        "plate_no": plate_no
    }

    response = requests.post(API_URL, json=payload)

    print("STATUS CODE:", response.status_code)
    print("RAW RESPONSE:", response.text)

    try:
        return response.json()
    except:
        return {"error": "Response is not JSON"}

if __name__ == "__main__":
    ocr_detected_plate = "٢ ١ ٦ ط ر ث"
    result = checkout_car(ocr_detected_plate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
