#find_car.py
import requests
plate_to_search = "ىممك"  # ضع هنا الرقم العربي للعربية اللي عايز تبحث عنها
url = f"http://127.0.0.1:8000/find?plate={plate_to_search}"

r = requests.get(url)
print(r.json())