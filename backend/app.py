from flask import Flask, request, jsonify
from flask_cors import CORS
import time

from config import DEBUG
from models import Alert, add_alert, alerts_store
from detection import SignatureEngine, AnomalyEngine, MLDetectionEngine

app = Flask(__name__)
app.config["DEBUG"] = DEBUG
CORS(app)

sig_engine = SignatureEngine()
anomaly_engine = AnomalyEngine()
ml_engine = MLDetectionEngine()

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "time": time.time()})

@app.route("/api/events", methods=["POST"])
def receive_events():
    try:
        data = request.get_json(force=True)
        if not isinstance(data, list):
            data = [data]

        total_alerts = 0
        for event in data:
            all_alerts = []

            all_alerts.extend(sig_engine.analyze(event))
            all_alerts.extend(anomaly_engine.analyze(event))
            all_alerts.extend(ml_engine.analyze(event))

            for a in all_alerts:
                alert = Alert(
                    level=a.get("level", "INFO"),
                    message=a.get("message", "Unknown alert"),
                    details={
                        "rule": a.get("rule"),
                        "event": event,
                        "score": a.get("score")
                    },
                    source="ids-engine"
                )
                add_alert(alert)
                total_alerts += 1

        return jsonify({"status": "ok", "received": len(data), "alerts_generated": total_alerts})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400

@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    limit = int(request.args.get("limit", 100))
    result = [a.to_dict() for a in list(alerts_store)[:limit]]
    return jsonify(result)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))   # Render se port le raha hai
    app.run(host="0.0.0.0", port=port)
