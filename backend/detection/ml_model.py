import os
import joblib

class MLDetectionEngine:
    """
    ML based IDS - yaha simple binary classifier assume kar rahe hain.
    Model ko pehle train karo aur model.pkl is folder me save karo.
    """
    def __init__(self):
        self.model = None
        self.threshold = 0.5  # probability threshold
        model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            print("[ML] Warning: model.pkl not found, ML engine disabled.")

    def _extract_features(self, event):
        protocol = event.get("protocol", "OTHER")
        proto_tcp = 1 if protocol == "TCP" else 0
        proto_udp = 1 if protocol == "UDP" else 0

        length = event.get("length", 0) or 0
        src_port = event.get("src_port", 0) or 0
        dst_port = event.get("dst_port", 0) or 0

        return [[length, src_port, dst_port, proto_tcp, proto_udp]]

    def analyze(self, event):
        alerts = []
        if not self.model:
            return alerts

        features = self._extract_features(event)
        prob = self.model.predict_proba(features)[0][1]

        if prob >= self.threshold:
            alerts.append({
                "level": "HIGH",
                "message": f"ML model flagged event as malicious (score={prob:.2f})",
                "rule": "ML_DETECTION",
                "score": float(prob)
            })

        return alerts
