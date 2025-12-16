from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timezone
import re

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False  # مهم عشان العربي يظهر صح

# ---------------------------
# CONNECT TO MONGO ATLAS
# ---------------------------
MONGO_URI = "mongodb+srv://smart_parking_db_user:Vn8giL043FP4hqow@cluster0.nwqhs2y.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["parking"]
cars_collection = db["cars"]

# ---------------------------
# HELPER – Normalize Arabic plate
# ---------------------------
def normalize_plate(plate):
    # Arabic Eastern digits
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    # Persian digits
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    table = str.maketrans(persian_digits, arabic_digits)
    # remove spaces and normalize digits
    return plate.translate(table).replace(" ", "")

# ---------------------------
# HELPER – Validate plate_no (Arabic + letters)
# ---------------------------
def valid_plate_no(plate_no):
    # يسمح بالأرقام العربية (٠-٩) والحروف العربية والمسافات
    return bool(re.fullmatch(r"[٠-٩\u0621-\u064A ]+", plate_no))

# ---------------------------
# 1) ADD CAR (POST)
# ---------------------------
@app.route("/add_car", methods=["POST"])
def add_car():
    data = request.json
    required = ["owner_name", "car_type", "color", "plate_no", "category"]

    # Check required fields
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Validate plate_no
    if not valid_plate_no(data["plate_no"]):
        return jsonify({"error": "plate_no must contain Arabic digits and letters only"}), 400

    # Normalize plate
    normalized_plate = normalize_plate(data["plate_no"])

    # Prevent duplicate registration
    existing_car = cars_collection.find_one({
        "$expr": {"$eq": [
            {"$replaceAll": {"input": "$plate_no", "find": " ", "replacement": ""}},
            normalized_plate
        ]}
    })
    if existing_car:
        return jsonify({"error": "Car with this plate_no already exists"}), 409

    # Add timestamp
    data["check_in"] = datetime.now(timezone.utc).isoformat()

    try:
        # Insert into MongoDB
        result = cars_collection.insert_one(data)

        response = {
            "status": "Car added successfully",
            "car_id": str(result.inserted_id),
            "owner_name": data["owner_name"],
            "car_type": data["car_type"],
            "color": data["color"],
            "plate_no": data["plate_no"],
            "category": data["category"],
            "check_in": data["check_in"]
        }
        return jsonify(response), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------
# 2) GET ALL CARS
# ---------------------------
@app.route("/cars", methods=["GET"])
def get_cars():
    cars = list(cars_collection.find({}, {"_id": 0}))
    return jsonify(cars)

# ---------------------------
# 3) SEARCH BY PLATE_NO
# ---------------------------
@app.route("/find", methods=["GET"])
def find_car():
    plate = request.args.get("plate")
    if not plate:
        return jsonify({"error": "plate parameter is required"}), 400

    normalized_plate = normalize_plate(plate)

    car = cars_collection.find_one({
        "$expr": {"$eq": [
            {"$replaceAll": {"input": "$plate_no", "find": " ", "replacement": ""}},
            normalized_plate
        ]}
    }, {"_id": 0})

    if not car:
        return jsonify({"message": "Car not found"}), 404

    return jsonify(car)

# ---------------------------
# 4) DELETE BY PLATE_NO
# ---------------------------
@app.route("/delete", methods=["DELETE"])
def delete_car():
    plate = request.args.get("plate")
    if not plate:
        return jsonify({"error": "plate parameter is required"}), 400

    normalized_plate = normalize_plate(plate)

    result = cars_collection.delete_one({
        "$expr": {"$eq": [
            {"$replaceAll": {"input": "$plate_no", "find": " ", "replacement": ""}},
            normalized_plate
        ]}
    })

    if result.deleted_count == 0:
        return jsonify({"message": "Car not found"}), 404

    return jsonify({"status": "Car deleted"})

# ---------------------------
# 5) RUN SERVER LOCALLY
# ---------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
