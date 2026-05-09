from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)

# ---------------- DATABASE ----------------
food_list = []

ngos = [
    {
        "name": "Helping Hands NGO",
        "lat": 18.5204,
        "lng": 73.8567,
        "preference": "veg"
    },
    {
        "name": "Food Care NGO",
        "lat": 18.5300,
        "lng": 73.8600,
        "preference": "non-veg"
    }
]

# ---------------- FRONTEND ----------------
@app.route('/')
def home():
    return render_template("index.html")

# ---------------- ADD FOOD ----------------
@app.route('/add-food', methods=['POST'])
def add_food():
    data = request.json

    food = {
        "name": data.get("name"),
        "location": data.get("location"),
        "quantity": data.get("quantity"),
        "phone": data.get("phone"),
        "lat": data.get("lat"),
        "lng": data.get("lng"),
        "type": data.get("type", "veg"),
        "user": data.get("user")
    }

    food_list.append(food)

    return jsonify({"message": "Food added successfully", "data": food})

# ---------------- GET FOOD ----------------
@app.route('/get-food')
def get_food():
    return jsonify(food_list)

# ---------------- CLAIM FOOD ----------------
@app.route('/claim-food', methods=['POST'])
def claim_food():
    index = request.json.get("index")

    if 0 <= index < len(food_list):
        removed = food_list.pop(index)
        return jsonify({"message": "Food claimed", "data": removed})

    return jsonify({"error": "Invalid index"}), 400

# ---------------- DISTANCE FUNCTION ----------------
def distance(lat1, lon1, lat2, lon2):
    return ((lat1 - lat2)**2 + (lon1 - lon2)**2) ** 0.5

# ---------------- SMART MATCHING (NO ML) ----------------
@app.route('/smart-match', methods=['POST'])
def smart_match():
    food = request.json

    best_ngo = None
    best_score = -1

    for ngo in ngos:
        score = 0

        # 1. distance scoring
        dist = distance(food["lat"], food["lng"], ngo["lat"], ngo["lng"])
        score += max(0, 100 - dist * 100)

        # 2. food preference match
        if food["type"] == ngo["preference"]:
            score += 50

        # 3. urgency boost
        score += food.get("urgency", 10)

        if score > best_score:
            best_score = score
            best_ngo = ngo

    return jsonify({
        "best_match": best_ngo,
        "score": best_score
    })

# ---------------- RUN ----------------

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8000)
