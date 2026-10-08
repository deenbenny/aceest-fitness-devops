from flask import Flask, jsonify, request

app = Flask(__name__)
members = []
PROGRAMS = {"fat_loss": "Fat Loss", "muscle_gain": "Muscle Gain", "beginner": "Beginner"}


def calculate_bmi(weight_kg, height_m):
    if weight_kg <= 0 or height_m <= 0:
        raise ValueError("weight and height must be positive")
    return round(weight_kg / (height_m ** 2), 2)


@app.get("/")
def home():
    return jsonify(message="Welcome to ACEest Fitness & Gym")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/programs")
def programs():
    return jsonify(PROGRAMS)


@app.route("/members", methods=["GET", "POST"])
def member_list():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        if not data.get("name") or data.get("program") not in PROGRAMS:
            return jsonify(error="name and valid program required"), 400
        members.append({"id": len(members) + 1, **data})
        return jsonify(members[-1]), 201
    return jsonify(members)


@app.post("/bmi")
def bmi():
    data = request.get_json(silent=True) or {}
    try:
        return jsonify(bmi=calculate_bmi(float(data["weight"]), float(data["height"])))
    except (KeyError, ValueError, TypeError) as e:
        return jsonify(error=str(e)), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
