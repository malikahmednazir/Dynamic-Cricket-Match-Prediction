from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "project": "Dynamic Cricket Match Prediction",
        "status": "Backend running"
    })

@app.route("/api/health")
def health():
    return jsonify({"status": "online"})

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}

    required = ["team1", "team2", "overs", "wickets"]
    missing = [x for x in required if x not in data]

    if missing:
        return jsonify({
            "error": "Missing fields",
            "fields": missing
        }), 400

    # Connect your existing trained model here.
    # Do not return fabricated prediction results.
    return jsonify({
        "status": "model_integration_required",
        "message": "Connect the existing trained cricket model before prediction."
    }), 501

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
