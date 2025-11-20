import statistics
import time

class AnomalyEngine:
    def __init__(self):
        self.window_size = 100
        self.lengths = []
        self.last_rate_calc_time = time.time()
        self.event_count = 0
        self.events_per_sec_baseline = None

    def analyze(self, event):
        alerts = []

        length = event.get("length", 0)
        self.lengths.append(length)
        if len(self.lengths) > self.window_size:
            self.lengths.pop(0)

        if len(self.lengths) >= 10:
            mean_len = statistics.mean(self.lengths)
            stdev_len = statistics.pstdev(self.lengths)

            if length > mean_len + 3 * stdev_len:
                alerts.append({
                    "level": "MEDIUM",
                    "message": f"Anomalous packet size: {length}",
                    "rule": "LARGE_PACKET_ANOMALY"
                })

        now = time.time()
        self.event_count += 1
        elapsed = now - self.last_rate_calc_time

        if elapsed >= 10:
            rate = self.event_count / elapsed
            if self.events_per_sec_baseline is None:
                self.events_per_sec_baseline = rate
            else:
                if rate > self.events_per_sec_baseline * 3:
                    alerts.append({
                        "level": "HIGH",
                        "message": f"Traffic rate anomaly: {rate:.2f} events/sec",
                        "rule": "TRAFFIC_SPIKE"
                    })
            self.last_rate_calc_time = now
            self.event_count = 0

        return alerts
