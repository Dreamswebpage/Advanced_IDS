import ipaddress

class SignatureEngine:
    def __init__(self):
        # Example signature rules
        self.blocked_ips = {
            "192.168.1.100",
            "10.0.0.5"
        }

        self.suspicious_ports = {22, 23, 3389}  # SSH, Telnet, RDP

        self.port_scan_threshold = 20
        self.connection_tracker = {}

    def analyze(self, event):
        alerts = []

        src_ip = event.get("src_ip")
        dst_port = event.get("dst_port")

        # Rule 1: known bad IP
        if src_ip in self.blocked_ips:
            alerts.append({
                "level": "HIGH",
                "message": f"Traffic from blocked IP {src_ip}",
                "rule": "BLOCKED_IP"
            })

        # Rule 2: suspicious destination port
        if dst_port in self.suspicious_ports:
            alerts.append({
                "level": "MEDIUM",
                "message": f"Traffic to suspicious port {dst_port}",
                "rule": "SUSPICIOUS_PORT"
            })

        # Rule 3: simple port scan detection
        if src_ip and dst_port:
            key = src_ip
            ports = self.connection_tracker.setdefault(key, set())
            ports.add(dst_port)
            if len(ports) > self.port_scan_threshold:
                alerts.append({
                    "level": "HIGH",
                    "message": f"Potential port scan from {src_ip}",
                    "rule": "PORT_SCAN"
                })

        return alerts
