# 🚨 Intrusion Detection System (IDS)

This project is a complete **Network Intrusion Detection System (IDS)** designed with three modular components:

1. **Agent** – Collects real-time network packets  
2. **Backend IDS Engine** – Processes events using Signature, Anomaly, and optional ML detection  
3. **Dashboard** – Displays live alerts in a modern and clean UI  

This is a full working IDS suitable for learning, experimentation, and understanding real-world detection pipelines.

---

## 🏗️ Project Structure

ids-project/
├── agent/
│ ├── agent.py
│ ├── config.py
│ └── requirements.txt
│
├── backend/
│ ├── app.py
│ ├── config.py
│ ├── requirements.txt
│ ├── detection/
│ │ ├── signatures.py
│ │ ├── anomaly.py
│ │ └── ml_model.py
│ └── models/
│ └── alert.py
│
└── dashboard/
├── index.html
├── css/
└── js/

markdown
Copy code

---

## ✨ Features

### 🔹 **Agent**
- Live packet sniffing using Scapy  
- Converts packets → structured JSON events  
- Batch sending to backend  
- Extracts IP/Ports/Protocol/Length  
- Low overhead and lightweight  

### 🔹 **Backend IDS Engine**
Includes **3-layer detection**:

#### 1. Signature-based Detection  
- Blocked IP rules  
- Suspicious port detection  
- Port scan tracking  

#### 2. Anomaly-based Detection  
- Abnormal packet size detection  
- Traffic spike anomaly  

#### 3. ML-based Detection (optional)  
- Loads pretrained `model.pkl`  
- Binary malicious event prediction  

#### Extra:
- In-memory alert storage  
- REST API for alerts, health, and ingest  

### 🔹 **Dashboard**
- Real-time alerts viewer  
- Auto-refresh toggle  
- Severity-based color coding  
- Backend health monitor  
- Lightweight static UI (HTML + JS)  

---

## 🚀 Getting Started

### 1️⃣ Start Backend (API Server)

```bash
cd backend
pip install -r requirements.txt
python app.py
Backend will run on:

cpp
Copy code
http://127.0.0.1:5000
2️⃣ Start the Agent (Packet Collector)
bash
Copy code
cd agent
pip install -r requirements.txt
sudo python agent.py
Windows PowerShell (Admin):

powershell
Copy code
python agent.py
❗ Edit agent/config.py to select correct network interface.

3️⃣ Open Dashboard (Static HTML)
Method 1: Python server

bash
Copy code
cd dashboard
python -m http.server 8080
Browser open:

cpp
Copy code
http://127.0.0.1:8080
Method 2: VS Code Live Server
Right-click → Open with Live Server

🧠 How It Works
🔹 Step 1 — Agent
Sniffs raw packets

Parses IP, port, protocol

Creates event dictionary

Sends batch JSON to backend every few seconds

🔹 Step 2 — Backend IDS Engine
Runs 3 detection engines:

✔ Signature Engine
Bad IP list

Dangerous ports

Port scanning behaviour

✔ Anomaly Engine
Moving window packet-size stats

Traffic rate monitoring

✔ ML Engine
Optional classifier (model.pkl)

Uses features:

csharp
Copy code
[length, src_port, dst_port, is_tcp, is_udp]
🔹 Step 3 — Dashboard
Fetches /api/alerts frequently

Renders alerts in table

Shows severity by color

📝 API Endpoints
➤ POST /api/events
Send events from agent.

Example payload:

json
Copy code
[
  {
    "src_ip": "192.168.1.10",
    "dst_ip": "10.0.0.5",
    "src_port": 443,
    "dst_port": 80,
    "protocol": "TCP",
    "length": 512,
    "timestamp": 1700000000
  }
]
➤ GET /api/alerts
Fetch recent alerts:

bash
Copy code
/api/alerts?limit=100
Response format:

json
Copy code
[
  {
    "id": 12345,
    "level": "HIGH",
    "message": "Traffic from blocked IP",
    "timestamp": 1700000000
  }
]
➤ GET /api/health
Backend health status.

🤖 Machine Learning (Optional)
To enable ML detection:

Train your ML model

Save it as model.pkl

Place it inside:

bash
Copy code
backend/detection/model.pkl
Your model must support:

python
Copy code
predict_proba()
🛡️ Future Enhancements
Database storage (MongoDB / PostgreSQL)

TLS encryption for Agent → Backend

Multi-agent distributed IDS

Real-time WebSocket alerts

Auto-learning anomaly model

SIEM integration

👨‍💻 Contributing
Submit PRs with proper commit messages:

vbnet
Copy code
feat: new feature
fix: bug fix
refactor: code improvement
docs: README update
📄 License
MIT License.

yaml
Copy code

---

Buddy, bas ye poora ek-shot README.md copy karke GitHub me paste kar dena.  
Agar tum chaaho to main:

🔥 README me **Badges**  
🔥 Project ka **ASCII logo**  
🔥 Screenshots add  
🔥 Hindi version  

bhi bana sakta hoon.
