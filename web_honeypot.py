from flask import Flask, request, render_template_string
from datetime import datetime, UTC
import json
import os
from genai_engine import generate_response
import re
from collections import defaultdict

app = Flask(__name__)

LOG_FILE = "data/logs.jsonl"
os.makedirs("data", exist_ok=True)

# Simple in-memory counter for brute-force detection
failed_attempts = defaultdict(int)

# Fake login page
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
</head>
<body>
    <h2>Admin Panel</h2>
    <p>Please login to continue</p>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required /><br><br>
        <input type="password" name="password" placeholder="Password" required /><br><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

# Simple attack pattern checks
SQLI_PATTERNS = [
    r"(\bor\b|\band\b).*(=|like)",
    r"union.*select",
    r"select.*from",
    r"drop\s+table",
    r"'--",
    r"\"--",
    r";--",
]

XSS_PATTERNS = [
    r"<script.*?>",
    r"javascript:",
    r"onerror=",
    r"onload=",
]

def is_sqli(payload: str) -> bool:
    payload = payload.lower()
    for pat in SQLI_PATTERNS:
        if re.search(pat, payload):
            return True
    return False

def is_xss(payload: str) -> bool:
    payload = payload.lower()
    for pat in XSS_PATTERNS:
        if re.search(pat, payload):
            return True
    return False

def log_event(event: dict):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

def analyze_request(ip, path, data_str):
    risk = 0
    tags = []

    if is_sqli(data_str):
        risk += 5
        tags.append("SQLi")

    if is_xss(data_str):
        risk += 5
        tags.append("XSS")

    # Brute-force detection
    if path in ["/admin", "/login"]:
        failed_attempts[ip] += 1
        if failed_attempts[ip] > 5:
            risk += 3
            tags.append("Bruteforce")

    # Simple scanner detection
    if any(p in path.lower() for p in ["phpmyadmin", "wp-admin", ".env", "config"]):
        risk += 2
        tags.append("Scanner")

    if risk == 0:
        tags.append("Low-Risk")

    return risk, tags

@app.route("/")
def index():
    return "Web Honeypot is running. Try /admin or /login"

@app.route("/admin", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def fake_login():
    # ✅ Use forwarded IP if present (for simulator)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "")
    timestamp = datetime.now(UTC).isoformat()
    
    # Extract country and location from headers
    country = request.headers.get("X-Country", "Unknown")
    lat = request.headers.get("X-Lat", "0")
    lon = request.headers.get("X-Lon", "0")

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        payload = f"{username} {password}"

        risk, tags = analyze_request(ip, request.path, payload)

        event = {
            "time": timestamp,
            "ip": ip,
            "country": country,
            "lat": float(lat) if lat != "0" else 0,
            "lon": float(lon) if lon != "0" else 0,
            "user_agent": ua,
            "path": request.path,
            "method": "POST",
            "username": username,
            "password": password,
            "risk_score": risk,
            "tags": tags
        }

        log_event(event)

        # Always fail login, but look real
        return "Invalid credentials. Please try again.", 401

    else:
        # Log GET access
        risk, tags = analyze_request(ip, request.path, "")
        event = {
            "time": timestamp,
            "ip": ip,
            "country": country,
            "lat": float(lat) if lat != "0" else 0,
            "lon": float(lon) if lon != "0" else 0,
            "user_agent": ua,
            "path": request.path,
            "method": "GET",
            "risk_score": risk,
            "tags": tags
        }
        log_event(event)

        return render_template_string(LOGIN_PAGE)

# Catch-all route for scanners and fuzzers
@app.route("/<path:any_path>", methods=["GET", "POST"])
def catch_all(any_path):
    # ✅ Use forwarded IP if present (for simulator)
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "")
    timestamp = datetime.now(UTC).isoformat()
    
    # Extract country and location from headers
    country = request.headers.get("X-Country", "Unknown")
    lat = request.headers.get("X-Lat", "0")
    lon = request.headers.get("X-Lon", "0")

    data_str = ""
    if request.method == "POST":
        data_str = request.get_data(as_text=True)

    risk, tags = analyze_request(ip, "/" + any_path, data_str)

    event = {
        "time": timestamp,
        "ip": ip,
        "country": country,
        "lat": float(lat) if lat != "0" else 0,
        "lon": float(lon) if lon != "0" else 0,
        "user_agent": ua,
        "path": "/" + any_path,
        "method": request.method,
        "data": data_str,
        "risk_score": risk,
        "tags": tags
    }

    log_event(event)

    # 🧠 Decide attack type from tags
    attack_type = "Normal"
    if isinstance(tags, list) and len(tags) > 0:
        attack_type = tags[0]

    # 🎭 Generate smart fake response
    fake_content = generate_response(attack_type, risk, "/" + any_path)

    return fake_content, 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
