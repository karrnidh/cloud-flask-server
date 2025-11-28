from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Stores logs in memory
logs = []


@app.route("/", methods=["GET"])
def home():
    return "✅ Cloud Flask Server is running"


@app.route("/log", methods=["POST"])
def log_data():
    """
    Example expected JSON:
    {
        "group_id": 1,
        "project": "fall_detection",
        "value": 0.95,
        "note": "no fall detected"
    }
    """
    data = request.get_json() or {}

    entry = {
        "id": len(logs) + 1,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "group_id": data.get("group_id"),
        "project": data.get("project"),
        "value": data.get("value"),
        "note": data.get("note"),
        "raw": data,  # full payload
    }

    logs.append(entry)
    print("New entry:", entry)

    return jsonify({"status": "ok", "entry": entry}), 201


@app.route("/log", methods=["GET"])
def get_all_logs():
    return jsonify(logs)


@app.route("/log/<int:group_id>", methods=["GET"])
def get_group_logs(group_id):
    filtered = [e for e in logs if e.get("group_id") == group_id]
    return jsonify(filtered)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
