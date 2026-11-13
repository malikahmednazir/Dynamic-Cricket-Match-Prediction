from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "project": "Dynamic Cricket Match Prediction",
        "status": "Backend online"
    })

@app.route("/api/health")
def health():
    return jsonify({"status": "online"})

@app.route("/api/project-info")
def project_info():
    return jsonify({
        "name": "Dynamic Cricket Match Prediction",
        "frontend": "Angular",
        "backend": "Python Flask",
        "model_status": "Integration pending"
    })

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}

    required = ["team1", "team2", "overs", "wickets"]
    missing = [field for field in required if field not in data]

    if missing:
        return jsonify({"error": "Missing fields", "fields": missing}), 400

    try:
        overs = float(data["overs"])
        wickets = int(data["wickets"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid overs or wickets"}), 400

    if not 0 <= overs <= 50 or not 0 <= wickets <= 10:
        return jsonify({"error": "Invalid match values"}), 400

    return jsonify({
        "status": "model_integration_required",
        "message": "Input received successfully, but the trained prediction model has not yet been connected."
    }), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
