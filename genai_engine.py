import random
from datetime import datetime, UTC

FAKE_FILES = [
    "users.db", "config.yaml", "backup.sql", "secrets.txt",
    "logs.txt", "app.py", "admin_panel.php"
]

FAKE_PASSWORDS = ["P@ssw0rd!", "admin123", "changeme", "root@123", "welcome1"]

def juicy_secrets():
    return f"""
# Leaked Secrets (FAKE)
DB_USER=admin
DB_PASS={random.choice(FAKE_PASSWORDS)}
API_KEY=sk-{random.randint(1000000,9999999)}
AWS_SECRET=AKIA{random.randint(10000000,99999999)}
LAST_ROTATED={datetime.now(UTC).isoformat()}
"""

def fake_ls():
    files = random.sample(FAKE_FILES, k=random.randint(3, len(FAKE_FILES)))
    return "\n".join(files)

def fake_error():
    errors = [
        "Permission denied.",
        "Access denied.",
        "Internal server error.",
        "Invalid request.",
        "Operation failed."
    ]
    return random.choice(errors)

def fake_account_locked():
    return "Account temporarily locked due to too many failed attempts."

def fake_admin_page():
    return f"""
<h2>Admin Dashboard</h2>
<p>Status: OK</p>
<p>Active Users: admin, backup, service</p>
<p>Last Backup: {random.randint(1,28)}/0{random.randint(1,9)}/2026</p>
"""

def generate_response(attack_type: str, risk_score: int, path: str):
    attack_type = attack_type or "Normal"

    # High-risk attackers get juicy bait
    if risk_score >= 5:
        if "Scanner" in attack_type or "SQLi" in attack_type or "XSS" in attack_type:
            return juicy_secrets()
        if "Bruteforce" in attack_type:
            return fake_account_locked()

    # Medium / low risk
    if "Scanner" in attack_type:
        return fake_ls()

    if "SQLi" in attack_type or "XSS" in attack_type:
        return fake_error()

    if "admin" in path.lower():
        return fake_admin_page()

    return fake_error()