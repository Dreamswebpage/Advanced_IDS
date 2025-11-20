from scapy.all import sniff, IP, TCP, UDP
import time
import json
import threading
import requests
from collections import deque
from config import BACKEND_URL, INTERFACE, BATCH_SIZE, SEND_INTERVAL

event_buffer = deque()

def packet_to_event(pkt):
    event = {
        "src_ip": None,
        "dst_ip": None,
        "src_port": None,
        "dst_port": None,
        "protocol": None,
        "length": len(pkt),
        "timestamp": time.time()
    }

    if IP in pkt:
        event["src_ip"] = pkt[IP].src
        event["dst_ip"] = pkt[IP].dst

        if TCP in pkt:
            event["protocol"] = "TCP"
            event["src_port"] = pkt[TCP].sport
            event["dst_port"] = pkt[TCP].dport
        elif UDP in pkt:
            event["protocol"] = "UDP"
            event["src_port"] = pkt[UDP].sport
            event["dst_port"] = pkt[UDP].dport
        else:
            event["protocol"] = "OTHER"
    else:
        event["protocol"] = "NON_IP"

    return event

def packet_handler(pkt):
    event = packet_to_event(pkt)
    event_buffer.append(event)

def sender_thread():
    while True:
        try:
            if len(event_buffer) >= BATCH_SIZE:
                batch = []
                for _ in range(min(BATCH_SIZE, len(event_buffer))):
                    batch.append(event_buffer.popleft())

                resp = requests.post(
                    BACKEND_URL,
                    data=json.dumps(batch),
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                print(f"[AGENT] Sent {len(batch)} events, status={resp.status_code}")
        except Exception as e:
            print(f"[AGENT] Error sending data: {e}")
        time.sleep(SEND_INTERVAL)

def start_sniffer():
    print(f"[AGENT] Starting sniffer on interface: {INTERFACE}")
    sniff(iface=INTERFACE, prn=packet_handler, store=False)

if __name__ == "__main__":
    t = threading.Thread(target=sender_thread, daemon=True)
    t.start()
    start_sniffer()
