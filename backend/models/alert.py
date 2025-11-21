import time
from collections import deque
from config import MAX_ALERTS


class Alert:
    def __init__(self, level, message, details=None, source="engine"):
        self.id = int(time.time() * 1000)
        self.level = level          # INFO, LOW, MEDIUM, HIGH, CRITICAL
        self.message = message
        self.details = details or {}
        self.source = source
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level,
            "message": self.message,
            "details": self.details,
            "source": self.source,
            "timestamp": self.timestamp
        }

alerts_store = deque(maxlen=MAX_ALERTS)

def add_alert(alert: Alert):
    alerts_store.appendleft(alert)

