from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os

from config import DEBUG
from models import Alert, add_alert, alerts_store
from detection import SignatureEngine, AnomalyEngine, MLDetectionEngine

app = Flask(__name__)
app.config["DEBUG"] = DEBUG

# Allow full CORS (Dashboard → Backend communication)
CORS(app)

# Engines
sig_engine = SignatureEngine()
anomaly_engine = AnomalyEngine()
ml_engine = MLDetectionEngine()

# -------------------------
# HEALTH CHECK ENDPOINT
# -------------------------
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "time": time.time()})


# -------------------------
# RECEIVE EVENTS FROM AGENT
# -------------------------
@app.route("/api/events", methods=["POST"])
def receive_events():
    try:
        data = request.get_json(force=True)
        if not isinstance(data, list):
            data = [data]

        total_alerts = 0

        for event in data:
            all_alerts = []

            # Run all engines
            all_alerts.extend(sig_engine.analyze(event))
            all_alerts.extend(anomaly_engine.analyze(event))
            all_alerts.extend(ml_engine.analyze(event))

            # Save alerts
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

        return jsonify({
            "status": "ok",
            "received": len(data),
            "alerts_generated": total_alerts
        })

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 400


# -------------------------
# FETCH ALERTS FOR DASHBOARD
# -------------------------
@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    limit = int(request.args.get("limit", 100))
    result = [a.to_dict() for a in list(alerts_store)[:limit]]
    return jsonify(result)


# -------------------------
# CLEAR ALL ALERTS (DASHBOARD BUTTON)
# -------------------------
@app.route("/api/alerts/clear", methods=["POST"])
def clear_alerts():
    alerts_store.clear()
    return jsonify({"status": "cleared", "total": 0})


# -------------------------
# RENDER DEPLOY RUNNER
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
