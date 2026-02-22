import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def normal_traffic():
    print("[*] Sending normal traffic...")
    requests.get(f"{BASE_URL}/")
    requests.get(f"{BASE_URL}/admin")
    requests.post(f"{BASE_URL}/admin", data={"username": "user", "password": "hello123"})

def brute_force():
    print("[*] Simulating brute-force attacks...")
    for i in range(10):
        requests.post(f"{BASE_URL}/admin", data={"username": "admin", "password": f"pass{i}"})
        time.sleep(0.2)

def sqli_attacks():
    print("[*] Sending SQLi payloads...")
    payloads = [
        "admin' OR '1'='1",
        "' OR '1'='1' --",
        "test' UNION SELECT 1,2,3 --",
        "admin' AND 1=1 --"
    ]
    for p in payloads:
        requests.post(f"{BASE_URL}/admin", data={"username": p, "password": "test"})
        time.sleep(0.2)

def xss_attacks():
    print("[*] Sending XSS payloads...")
    payloads = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "\"><script>alert('x')</script>"
    ]
    for p in payloads:
        requests.post(f"{BASE_URL}/admin", data={"username": p, "password": "test"})
        time.sleep(0.2)

def scanner_probes():
    print("[*] Simulating scanner probes...")
    paths = [
        "/phpmyadmin",
        "/wp-admin",
        "/.env",
        "/config",
        "/test123",
        "/backup",
        "/admin.php"
    ]
    for path in paths:
        requests.get(f"{BASE_URL}{path}")
        time.sleep(0.2)

if __name__ == "__main__":
    print("🚨 Starting automated attack simulation against honeypot...\n")

    normal_traffic()
    brute_force()
    sqli_attacks()
    xss_attacks()
    scanner_probes()

    print("\n✅ Attack simulation completed. Check your dashboard and logs!")