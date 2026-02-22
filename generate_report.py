#!/usr/bin/env python3
"""
Cognitive Honeypot - Professional Security Report Generator
Generates a comprehensive, detailed PDF report with attack analysis and mitigation strategies
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, 
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus.flowables import KeepInFrame
import os
import datetime
from collections import Counter

# ============================================================================
# CONFIGURATION
# ============================================================================

LOG_FILE = "data/logs.jsonl"
PDF_OUT = "data/report.pdf"
CHARTS_DIR = "data/charts"

# Color Palette - Professional Security Theme
COLORS = {
    'primary': '#0f172a',       # Slate 900 - Dark navy
    'secondary': '#1e40af',     # Blue 800
    'accent': '#0ea5e9',       # Sky 500
    'success': '#059669',      # Emerald 600
    'warning': '#d97706',      # Amber 600
    'danger': '#dc2626',       # Red 600
    'dark': '#1e293b',         # Slate 800
    'light': '#f1f5f9',       # Slate 100
    'muted': '#64748b',       # Slate 500
    'white': '#ffffff',
    'background': '#f8fafc',   # Slate 50
    'border': '#e2e8f0',      # Slate 200
}

# ============================================================================
# MITIGATION GUIDES
# ============================================================================

MITIGATION_GUIDES = {
    "SQLi": {
        "severity": "CRITICAL",
        "description": """
        SQL Injection (SQLi) is a code injection technique that exploits security vulnerabilities in an 
        application's database layer. This occurs when user input is incorrectly filtered or not strongly 
        typed and is concatenated into database queries. Attackers can manipulate SQL queries to gain 
        unauthorized access to sensitive data, modify or delete database contents, or execute administrative 
        operations on the database.
        """,
        "impacts": [
            "Unauthorized access to sensitive database contents",
            "Data breach and exfiltration of customer information",
            "Modification or deletion of critical data",
            "Database user privilege escalation",
            "Potential complete system compromise through database OS-level access"
        ],
        "steps": [
            ("Use Parameterized Queries", 
             "Always use parameterized queries (prepared statements) instead of string concatenation. "
             "This ensures user input is always treated as data, not executable code."),
            ("Implement Input Validation",
             "Validate all user inputs using both allowlist and denylist approaches. "
             "Use strict type checking and format validation for all parameters."),
            ("Apply Least Privilege",
             "Database accounts used by applications should have minimal necessary permissions. "
             "Avoid using admin/superuser accounts for routine operations."),
            ("Use Web Application Firewall (WAF)",
             "Deploy a WAF to detect and block SQL injection attempts in real-time. "
             "Configure rules to identify common SQLi patterns."),
            ("Escape Special Characters",
             "If parameterized queries aren't possible, use proper escaping functions "
             "specific to your database system (e.g., mysqli_real_escape_string)."),
            ("Regular Security Testing",
             "Conduct regular penetration testing and code reviews to identify and fix "
             "SQL injection vulnerabilities before attackers find them."),
            ("Use ORM Frameworks",
             "Consider using Object-Relational Mapping (ORM) frameworks that handle SQL safely "
             "and reduce the risk of injection vulnerabilities.")
        ]
    },
    "XSS": {
        "severity": "HIGH",
        "description": """
        Cross-Site Scripting (XSS) is a type of computer security vulnerability typically found in web 
        applications which allow code injection by malicious web users into webpages viewed by other users. 
        Examples of such code include HTML code and client-side scripts. XSS attacks can steal session 
        cookies, credentials, perform actions on behalf of users, or inject malicious content.
        """,
        "impacts": [
            "Session hijacking through stolen cookies",
            "Credential theft via fake login forms",
            "Malicious redirects to phishing sites",
            "Keylogging and user activity monitoring",
            "Website defacement and content manipulation"
        ],
        "steps": [
            ("Implement Content Security Policy (CSP)",
             "Configure CSP headers to restrict script sources and prevent inline script execution. "
             "This is the most effective defense against XSS."),
            ("Output Encoding",
             "Encode all user-generated content before displaying it in browsers. "
             "Use context-appropriate encoding (HTML, URL, JavaScript, CSS)."),
            ("Use HTTPOnly Cookies",
             "Set the HTTPOnly flag on session cookies to prevent JavaScript access. "
             "This prevents stolen cookies from being used by attackers."),
            ("Input Validation",
             "Validate and sanitize all user inputs. Remove or neutralize potentially dangerous "
             "HTML tags like <script>, <iframe>, <object>."),
            ("Use Anti-XSS Libraries",
             "Implement sanitization libraries like DOMPurify (JavaScript), bleach (Python), "
             "or HTMLSanitizer to safely handle HTML content."),
            ("Avoid Dangerous APIs",
             "Never use innerHTML, document.write(), or eval() with user input. "
             "Use textContent, innerText, or safe DOM APIs instead."),
            ("Enable X-XSS-Protection",
             "Set the X-XSS-Protection header in HTTP responses for additional "
             "browser-based XSS filtering.")
        ]
    },
    "Bruteforce": {
        "severity": "HIGH",
        "description": """
        Brute Force attacks are a class of attacks where attackers systematically check all possible 
        combinations of passwords or encryption keys until the correct one is found. These attacks 
        exploit weak passwords and target authentication mechanisms to gain unauthorized access to accounts 
        or systems. They can be enhanced with dictionaries of common passwords (dictionary attacks) 
        or rules-based approaches.
        """,
        "impacts": [
            "Unauthorized account access",
            "Compromised user credentials",
            "Service disruption through account lockouts",
            "Lateral movement within the network",
            "Potential data breaches from compromised accounts"
        ],
        "steps": [
            ("Implement Account Lockout",
             "After 3-5 failed login attempts, temporarily lock the account for 15-30 minutes. "
             "Notify users via email or SMS of the lockout."),
            ("Use Multi-Factor Authentication (MFA)",
             "Require additional verification methods beyond passwords: SMS, email, "
             "authenticator apps, hardware tokens, or biometrics."),
            ("Rate Limiting",
             "Limit login attempts from a single IP address (e.g., 5 attempts per minute). "
             "Use progressive delays between attempts."),
            ("Implement CAPTCHA",
             "After failed attempts, require CAPTCHA verification to prevent automated attacks."),
            ("Strong Password Policy",
             "Enforce minimum 12-character passwords with complexity requirements. "
             "Prohibit common passwords using compromised credential databases."),
            ("Monitor and Alert",
             "Set up alerts for unusual login patterns, multiple failed attempts, "
             "and successful logins from unusual locations."),
            ("Use IP Reputation",
             "Block or challenge traffic from known malicious IP addresses and proxy networks.")
        ]
    },
    "Scanner": {
        "severity": "MEDIUM",
        "description": """
        Security scanners and reconnaissance tools automatically scan websites and networks for known 
        vulnerabilities, misconfigurations, and exposed files. While sometimes used legitimately for 
        security assessments, these tools are frequently used by attackers as reconnaissance to 
        identify potential targets and vulnerabilities before launching more serious attacks.
        """,
        "impacts": [
            "Discovery of application vulnerabilities",
            "Exposure of sensitive files and directories",
            "Information disclosure about technology stack",
            "Mapping of application attack surface",
            "Identification of outdated or vulnerable components"
        ],
        "steps": [
            ("Deploy Web Application Firewall (WAF)",
             "Monitor and block scanning activities in real-time. Configure rules to detect "
             "and respond to automated scanning tools."),
            ("Implement Rate Limiting",
             "Limit requests per IP to prevent automated scanning. Set thresholds for "
             "unusual request volumes."),
            ("Use Honeypot Pages",
             "Create trap pages with hidden links that legitimate users won't access but "
             "scanners will discover, alerting you to scanning."),
            ("Disable Directory Listing",
             "Configure web servers to prevent automatic directory listing. Ensure directories "
             "don't expose their contents."),
            ("Remove Version Information",
             "Remove server version and technology stack information from HTTP headers, "
             "error pages, and HTML comments."),
            ("Implement IDS/IPS",
             "Deploy Intrusion Detection/Prevention systems to monitor for suspicious "
             "patterns and automated tools."),
            ("Regular Vulnerability Scanning",
             "Proactively scan your own systems to find and fix vulnerabilities before attackers do.")
        ]
    },
    "Traversal": {
        "severity": "HIGH",
        "description": """
        Path Traversal (also known as Directory Traversal) attacks exploit vulnerabilities in 
        applications that use file paths in an unsafe manner. By manipulating file paths using 
        sequences like '../' or '..\\', attackers can access files and directories outside the 
        web root folder, potentially exposing sensitive system files, configuration files, and 
        private data.
        """,
        "impacts": [
            "Unauthorized access to system files (/etc/passwd, /etc/shadow)",
            "Exposure of configuration files with credentials",
            "Access to application source code",
            "Reading log files containing sensitive information",
            "Potential command execution through uploaded files"
        ],
        "steps": [
            ("Validate and Sanitize Input",
             "Check all file path inputs for traversal sequences (../, ..\\, %2e%2e). "
             "Reject or completely neutralize these patterns."),
            ("Use chroot Jails",
             "Run web servers in chroot environments to isolate the file system "
             "and limit accessible directories."),
            ("Implement Least Privilege",
             "Ensure the web server process has minimal file system access. "
             "Use read-only directories where possible."),
            ("Use Allowlist Approach",
             "Only permit access to specific, predefined files and directories. "
             "Never allow arbitrary file paths from user input."),
            ("Avoid Direct File Paths",
             "Use indirect references like file IDs or encrypted tokens instead of "
             "actual file paths in URLs."),
            ("Disable Server-Side Includes (SSI)",
             "Turn off SSI and CGI unless explicitly required for the application."),
            ("Use read-only File Storage",
             "Store user-accessible files in read-only directories when possible.")
        ]
    },
    "Command Injection": {
        "severity": "CRITICAL",
        "description": """
        Command Injection is an attack in which the goal is execution of arbitrary commands on the host 
        operating system via a vulnerable application. These attacks occur when an application passes 
        unsafe user input (forms, cookies, HTTP headers, etc.) to a system shell. In the most serious 
        cases, command injection can completely compromise the server and all data it contains.
        """,
        "impacts": [
            "Complete server compromise",
            "Installation of malware or ransomware",
            "Data exfiltration and theft",
            "Creation of backdoors for persistent access",
            "Lateral movement to other systems in the network"
        ],
        "steps": [
            ("Avoid System Calls",
             "Never use system(), exec(), shell_exec(), popen(), or similar functions "
             "that execute shell commands with user input."),
            ("Use Language APIs",
             "Use language-specific APIs for file operations, network requests, etc., "
             "instead of shell commands."),
            ("Strict Input Validation",
             "Validate all user input strictly using allowlists of permitted values. "
             "Reject anything that doesn't match expected patterns."),
            ("Escape Arguments",
             "If shell commands are unavoidable, properly escape all user input using "
             "language-specific escaping functions (e.g., shlex.quote)."),
            ("Apply Least Privilege",
             "Run web applications with minimal system privileges. Use dedicated service accounts."),
            ("Use Sandboxing",
             "Run commands in isolated containers or sandboxes (Docker, gvisor) "
             "to limit the blast radius of any compromise."),
            ("Command Whitelisting",
             "Only allow specific, predefined commands to be executed. "
             "Never construct command strings from user input.")
        ]
    },
    "Low-Risk": {
        "severity": "LOW",
        "description": """
        Low-risk activities include requests that don't pose immediate threats but should still be 
        monitored. These may include reconnaissance attempts, probe requests, or benign requests that 
        trigger security alerts. While not immediately dangerous, patterns in these activities can 
        indicate future attacks or identify vulnerabilities that need addressing.
        """,
        "impacts": [
            "Potential future targeted attacks",
            "Information gathering about the system",
            "Testing of security defenses",
            "Identification of weak points in the infrastructure"
        ],
        "steps": [
            ("Continue Monitoring",
             "Maintain comprehensive logging of all requests, including low-risk ones, "
             "to identify patterns over time."),
            ("Regular Log Analysis",
             "Periodically review low-risk logs to identify patterns that may indicate "
             "reconnaissance or preparation for attacks."),
            ("Maintain Patches",
             "Keep all software, libraries, and dependencies up-to-date with the latest "
             "security patches, even for low-severity vulnerabilities."),
            ("Defense in Depth",
             "Implement multiple layers of security controls. What seems low-risk today "
             "may become critical with new vulnerability disclosures."),
            ("Security Awareness",
             "Train developers and administrators about security best practices and "
             "emerging threats.")
        ]
    }
}

# ============================================================================
# STYLES AND FORMATTING
# ============================================================================

def create_styles():
    """Create custom paragraph styles for the report"""
    styles = getSampleStyleSheet()
    
    # Title
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Title'],
        fontSize=32,
        textColor=colors.HexColor(COLORS['primary']),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Cover Subtitle
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.HexColor(COLORS['secondary']),
        spaceAfter=40,
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))
    
    # Section Header
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor(COLORS['primary']),
        spaceBefore=25,
        spaceAfter=15,
        fontName='Helvetica-Bold',
        borderPadding=10
    ))
    
    # Subsection Header
    styles.add(ParagraphStyle(
        name='SubsectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor(COLORS['secondary']),
        spaceBefore=15,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    ))
    
    # Body Text
    styles.add(ParagraphStyle(
        name='ReportBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor(COLORS['dark']),
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        leading=16,
        wordWrap='CJK'
    ))
    
    # Justified Body
    styles.add(ParagraphStyle(
        name='ReportBodyLeft',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor(COLORS['dark']),
        spaceAfter=10,
        alignment=TA_LEFT,
        leading=14,
        wordWrap='CJK'
    ))
    
    # Table Header
    styles.add(ParagraphStyle(
        name='TableHeader',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.white,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Table Cell
    styles.add(ParagraphStyle(
        name='TableCell',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor(COLORS['dark']),
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))
    
    # Mitigation Step
    styles.add(ParagraphStyle(
        name='MitigationStep',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor(COLORS['dark']),
        spaceAfter=8,
        alignment=TA_LEFT,
        leading=13,
        leftIndent=5,
        bulletIndent=10,
        wordWrap='CJK'
    ))
    
    # Footer
    styles.add(ParagraphStyle(
        name='ReportFooter',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor(COLORS['muted']),
        alignment=TA_CENTER
    ))
    
    return styles

# ============================================================================
# DATA LOADING
# ============================================================================

def load_logs():
    """Load and process log data"""
    rows = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except:
                continue
    df = pd.DataFrame(rows)
    
    # Process tags to get attack type
    def get_attack_type(tags):
        try:
            if pd.isna(tags).any() if hasattr(pd.isna(tags), 'any') else pd.isna(tags):
                return "Low-Risk"
        except:
            pass
        
        if not isinstance(tags, list):
            tags = [tags]
        
        # Handle numpy arrays or pandas series
        if hasattr(tags, 'tolist'):
            tags = tags.tolist() # type: ignore
            
        tags_str = str(list(tags)).lower()
        
        if 'sqli' in tags_str:
            return "SQLi"
        elif 'xss' in tags_str:
            return "XSS"
        elif 'bruteforce' in tags_str:
            return "Bruteforce"
        elif 'traversal' in tags_str:
            return "Traversal"
        elif 'scanner' in tags_str:
            return "Scanner"
        elif 'injection' in tags_str or 'cmd' in tags_str:
            return "Command Injection"
        else:
            return "Low-Risk"
    
    if 'tags' in df.columns:
        df['attack_type'] = df['tags'].apply(get_attack_type)
    
    return df

# ============================================================================
# CHART GENERATION
# ============================================================================

def generate_charts(df):
    """Generate all charts for the report"""
    os.makedirs(CHARTS_DIR, exist_ok=True)
    chart_paths = []
    
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # 1. Attack Types Pie Chart
    if 'attack_type' in df.columns:
        plt.figure(figsize=(8, 6))
        attack_counts = df['attack_type'].value_counts()
        colors_pie = [COLORS['danger'], COLORS['warning'], COLORS['secondary'], 
                     COLORS['accent'], COLORS['success'], COLORS['muted'], COLORS['primary']]
        result = plt.pie(
            attack_counts.values, 
            labels=attack_counts.index,
            autopct='%1.1f%%',
            colors=colors_pie[:len(attack_counts)],
            explode=[0.02] * len(attack_counts),
            shadow=True,
            startangle=90
        )
        # Handle tuple unpacking - may return 2 or 3 values depending on matplotlib version
        if len(result) >= 3:
            wedges, texts, autotexts = result[:3]
        else:
            wedges, texts = result[:2]
            autotexts = texts
        plt.setp(texts, size=10)
        plt.title("Attack Types Distribution", fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        path = f"{CHARTS_DIR}/attack_types_pie.png"
        plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        chart_paths.append(path)
    
    # 2. Top IPs Bar Chart
    if 'ip' in df.columns:
        plt.figure(figsize=(10, 5))
        top_ips = df['ip'].value_counts().head(10)
        colors_bar = [COLORS['primary'], COLORS['secondary'], COLORS['accent'],
                     COLORS['danger'], COLORS['warning'], COLORS['success'],
                     COLORS['muted'], COLORS['primary'], COLORS['secondary'], COLORS['accent']]
        bars = plt.barh(range(len(top_ips)), top_ips.values, color=colors_bar[:len(top_ips)])
        plt.yticks(range(len(top_ips)), top_ips.index)
        plt.xlabel('Number of Attacks', fontsize=10)
        plt.ylabel('IP Address', fontsize=10)
        plt.title('Top 10 Attacking IP Addresses', fontsize=14, fontweight='bold', pad=15)
        plt.gca().invert_yaxis()
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, top_ips.values)):
            plt.text(val + 5, i, str(val), va='center', fontsize=8)
        
        plt.tight_layout()
        path = f"{CHARTS_DIR}/top_ips.png"
        plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        chart_paths.append(path)
    
    # 3. Risk Distribution
    if 'risk_score' in df.columns:
        plt.figure(figsize=(8, 5))
        risk_counts = df['risk_score'].value_counts().sort_index()
        colors_risk = [COLORS['success'], COLORS['success'], COLORS['warning'],
                      COLORS['warning'], COLORS['danger'], COLORS['danger'],
                      COLORS['danger'], COLORS['danger'], COLORS['danger'], COLORS['danger'], COLORS['danger']]
        
        bars = plt.bar(risk_counts.index, risk_counts.values, color=colors_risk[:len(risk_counts)])
        plt.xlabel('Risk Score (0 = Low, 10 = Critical)', fontsize=10)
        plt.ylabel('Number of Events', fontsize=10)
        plt.title('Risk Score Distribution', fontsize=14, fontweight='bold', pad=15)
        plt.xticks(range(11))
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        path = f"{CHARTS_DIR}/risk_distribution.png"
        plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        chart_paths.append(path)
    
    # 4. Attacks by Country
    if 'country' in df.columns:
        plt.figure(figsize=(10, 5))
        countries = df[df['country'] != 'Unknown']['country'].value_counts().head(10)
        colors_country = [COLORS['primary'], COLORS['secondary'], COLORS['accent'],
                         COLORS['warning'], COLORS['danger'], COLORS['success'],
                         COLORS['muted'], COLORS['primary'], COLORS['secondary'], COLORS['accent']]
        
        bars = plt.barh(range(len(countries)), countries.values, color=colors_country[:len(countries)])
        plt.yticks(range(len(countries)), countries.index)
        plt.xlabel('Number of Attacks', fontsize=10)
        plt.ylabel('Country', fontsize=10)
        plt.title('Attacks by Country (Top 10)', fontsize=14, fontweight='bold', pad=15)
        plt.gca().invert_yaxis()
        
        for i, (bar, val) in enumerate(zip(bars, countries.values)):
            plt.text(val + 5, i, str(val), va='center', fontsize=8)
        
        plt.tight_layout()
        path = f"{CHARTS_DIR}/attacks_by_country.png"
        plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        chart_paths.append(path)
    
    # 5. Attack Timeline
    if 'time' in df.columns:
        plt.figure(figsize=(12, 4))
        df['time_parsed'] = pd.to_datetime(df['time'], errors='coerce')
        df['hour'] = df['time_parsed'].dt.strftime('%H:00')
        timeline = df['hour'].value_counts().sort_index()
        
        plt.plot(timeline.index, timeline.values, marker='o', linewidth=2, 
                markersize=4, color=COLORS['primary'])
        plt.fill_between(timeline.index, timeline.values, alpha=0.3, color=COLORS['accent'])
        plt.xlabel('Time (Hour)', fontsize=10)
        plt.ylabel('Number of Attacks', fontsize=10)
        plt.title('Attack Timeline', fontsize=14, fontweight='bold', pad=15)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        path = f"{CHARTS_DIR}/timeline.png"
        plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        chart_paths.append(path)
    
    return chart_paths

# ============================================================================
# PDF HEADER/FOOTER
# ============================================================================

def create_header(canvas, doc):
    """Draw header on each page"""
    canvas.saveState()
    page_width, page_height = A4
    
    # Header bar
    canvas.setFillColor(colors.HexColor(COLORS['primary']))
    canvas.rect(0, page_height - 40, page_width, 40, fill=1, stroke=0)
    
    # Logo/Title
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(50, page_height - 26, "🛡️ Cognitive Honeypot")
    
    # Document title
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor('#94a3b8'))
    canvas.drawRightString(page_width - 50, page_height - 26, "Security Analysis Report")
    
    # Bottom line
    canvas.setStrokeColor(colors.HexColor(COLORS['secondary']))
    canvas.setLineWidth(2)
    canvas.line(0, page_height - 40, page_width, page_height - 40)
    
    canvas.restoreState()

def create_footer(canvas, doc):
    """Draw footer on each page"""
    canvas.saveState()
    page_width, page_height = A4
    
    # Top line
    canvas.setStrokeColor(colors.HexColor(COLORS['border']))
    canvas.setLineWidth(1)
    canvas.line(50, page_height - 50, page_width - 50, page_height - 50)
    
    # Page number
    canvas.setFillColor(colors.HexColor(COLORS['muted']))
    canvas.setFont("Helvetica", 9)
    page_num = canvas.getPageNumber()
    canvas.drawString(50, 30, f"Page {page_num}")
    
    # Generated timestamp
    canvas.drawRightString(page_width - 50, 30, 
                          f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    canvas.restoreState()

# ============================================================================
# PDF CONTENT BUILDERS
# ============================================================================

def build_cover_page(story, styles, df, total):
    """Build the cover page"""
    story.append(Spacer(1, 2 * inch))
    
    # Main Title
    story.append(Paragraph("🛡️ Cognitive Honeypot", styles['ReportTitle']))
    story.append(Paragraph("Comprehensive Security Analysis Report", styles['CoverSubtitle']))
    
    story.append(Spacer(1, 0.5 * inch))
    
    # Date
    story.append(Paragraph(
        f"Generated: {datetime.datetime.now().strftime('%B %d, %Y at %H:%M')}",
        ParagraphStyle('Date', parent=styles['Normal'], fontSize=12, 
                      textColor=colors.HexColor(COLORS['muted']), alignment=TA_CENTER)
    ))
    
    story.append(Spacer(1, 1.5 * inch))
    
    # Executive Summary Box
    summary_data = [
        ['', '', '', '']
    ]
    
    # Calculate metrics
    total_attacks = len(df)
    unique_ips = df['ip'].nunique() if 'ip' in df.columns else 0
    high_risk = len(df[df['risk_score'] >= 7]) if 'risk_score' in df.columns else 0
    avg_risk = f"{df['risk_score'].mean():.1f}" if 'risk_score' in df.columns and len(df) > 0 else "N/A"
    
    # Summary table
    summary = Table([
        ['Total Events', 'Unique Attackers', 'High Risk Events', 'Avg Risk'],
        [str(total_attacks), str(unique_ips), str(high_risk), avg_risk]
    ], colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    
    summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['secondary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 16),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor(COLORS['light'])),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(COLORS['border'])),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(summary)
    
    story.append(Spacer(1, 2 * inch))
    
    # Classification notice
    story.append(Paragraph(
        "⚠️ CONFIDENTIAL SECURITY DOCUMENT",
        ParagraphStyle('Warning', parent=styles['Normal'], fontSize=14, 
                     textColor=colors.HexColor(COLORS['danger']), alignment=TA_CENTER,
                     fontName='Helvetica-Bold')
    ))
    story.append(Paragraph(
        "This report contains sensitive security information and is intended solely for authorized personnel. "
        "Handle and store in accordance with your organization's security policies.",
        ParagraphStyle('Warning2', parent=styles['Normal'], fontSize=10, 
                     textColor=colors.HexColor(COLORS['muted']), alignment=TA_CENTER)
    ))
    
    story.append(PageBreak())

def build_table_of_contents(story, styles):
    """Build table of contents"""
    story.append(Paragraph("Table of Contents", styles['SectionHeader']))
    story.append(Spacer(1, 0.2 * inch))
    
    toc_items = [
        ("1.", "Executive Summary", "3"),
        ("2.", "Attack Overview and Statistics", "4"),
        ("3.", "Top Attacking IP Addresses", "5"),
        ("4.", "Attack Visualizations", "6"),
        ("5.", "Risk Assessment Analysis", "7"),
        ("6.", "Detailed Attack Mitigation Guide", "8"),
        ("7.", "Security Recommendations", "12"),
        ("8.", "Appendix: Document Information", "14"),
    ]
    
    for num, title, page in toc_items:
        story.append(Paragraph(
            f"<b>{num}</b> {title} ............................ {page}",
            ParagraphStyle('TOC', parent=styles['Normal'], fontSize=11,
                          spaceAfter=8, leftIndent=20)
        ))
    
    story.append(PageBreak())

def build_executive_summary(story, styles, df):
    """Build executive summary section"""
    story.append(Paragraph("1. Executive Summary", styles['SectionHeader']))
    
    story.append(Paragraph(
        "This report provides a comprehensive analysis of the security events captured by the Cognitive "
        "Honeypot system. The data presented herein encompasses all detected attack attempts, "
        "including their origin, type, severity, and potential impact on the protected infrastructure.",
        styles['ReportBody']
    ))
    
    story.append(Spacer(1, 0.2 * inch))
    
    # Key findings
    story.append(Paragraph("Key Findings:", styles['SubsectionHeader']))
    
    total = len(df)
    if 'attack_type' in df.columns:
        top_attack = df['attack_type'].value_counts().head(1)
        if len(top_attack) > 0:
            story.append(Paragraph(
                f"• The most prevalent attack type observed was <b>{top_attack.index[0]}</b> "
                f"({top_attack.values[0]} events, {top_attack.values[0]/total*100:.1f}%)",
                styles['ReportBodyLeft']
            ))
    
    if 'ip' in df.columns:
        top_ip = df['ip'].value_counts().head(1)
        if len(top_ip) > 0:
            story.append(Paragraph(
                f"• The most active attacking IP was <b>{top_ip.index[0]}</b> with "
                f"{top_ip.values[0]} attack attempts",
                styles['ReportBodyLeft']
            ))
    
    if 'risk_score' in df.columns:
        high_risk = len(df[df['risk_score'] >= 7])
        story.append(Paragraph(
            f"• <b>{high_risk}</b> events ({high_risk/total*100:.1f}%) were classified as "
            f"high-risk (score ≥ 7), requiring immediate attention",
            styles['ReportBodyLeft']
        ))
    
    story.append(Spacer(1, 0.3 * inch))
    
    # Attack type breakdown
    if 'attack_type' in df.columns:
        story.append(Paragraph("Attack Type Breakdown:", styles['SubsectionHeader']))
        
        attack_counts = df['attack_type'].value_counts()
        
        data = [['Attack Type', 'Count', 'Percentage', 'Risk Level']]
        for attack_type, count in attack_counts.items():
            risk = "CRITICAL" if attack_type in ['SQLi', 'Command Injection'] else \
                   "HIGH" if attack_type in ['XSS', 'Bruteforce'] else \
                   "MEDIUM" if attack_type in ['Traversal', 'Scanner'] else "LOW"
            data.append([attack_type, str(count), f"{count/total*100:.1f}%", risk])
        
        table = Table(data, colWidths=[1.8*inch, 1*inch, 1*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['primary'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor(COLORS['border'])),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(table)

def build_top_ips(story, styles, df):
    """Build top attacking IPs section"""
    story.append(PageBreak())
    story.append(Paragraph("3. Top Attacking IP Addresses", styles['SectionHeader']))
    
    if 'ip' not in df.columns:
        return
    
    top_ips = df['ip'].value_counts().head(15)
    
    data = [['Rank', 'IP Address', 'Attacks', 'Avg Risk', 'Country', 'Primary Attack']]
    
    for i, (ip, count) in enumerate(top_ips.items(), 1):
        ip_df = df[df['ip'] == ip]
        avg_risk = f"{ip_df['risk_score'].mean():.1f}"
        country = ip_df['country'].iloc[0] if 'country' in ip_df.columns else "Unknown"
        primary = ip_df['attack_type'].mode().iloc[0] if 'attack_type' in ip_df.columns else "N/A"
        
        data.append([str(i), ip, str(count), avg_risk, country[:12], primary[:12]])
    
    table = Table(data, colWidths=[0.4*inch, 1.8*inch, 0.7*inch, 0.6*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['secondary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor(COLORS['border'])),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(table)

def build_visualizations(story, styles, charts):
    """Build visualizations section"""
    story.append(PageBreak())
    story.append(Paragraph("4. Attack Visualizations", styles['SectionHeader']))
    
    chart_names = [
        "Attack Types Distribution",
        "Top Attacking IP Addresses", 
        "Risk Score Distribution",
        "Attacks by Country",
        "Attack Timeline"
    ]
    
    for i, chart_path in enumerate(charts):
        story.append(Paragraph(chart_names[i] if i < len(chart_names) else f"Chart {i+1}", 
                              styles['SubsectionHeader']))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Image(chart_path, width=6*inch, height=3*inch))
        story.append(Spacer(1, 0.2 * inch))

def build_risk_assessment(story, styles, df):
    """Build risk assessment section"""
    story.append(PageBreak())
    story.append(Paragraph("5. Risk Assessment Analysis", styles['SectionHeader']))
    
    if 'risk_score' not in df.columns:
        return
    
    total = len(df)
    critical = len(df[df['risk_score'] >= 9])
    high = len(df[(df['risk_score'] >= 7) & (df['risk_score'] < 9)])
    medium = len(df[(df['risk_score'] >= 4) & (df['risk_score'] < 7)])
    low = len(df[df['risk_score'] < 4])
    
    # Risk breakdown
    data = [
        ['Risk Level', 'Count', 'Percentage', 'Description'],
        [f'🔴 Critical (9-10)', str(critical), f'{critical/total*100:.1f}%', 
         'Immediate threat - likely active attack'],
        [f'🟠 High (7-8)', str(high), f'{high/total*100:.1f}%', 
         'Serious threat - requires urgent attention'],
        [f'🟡 Medium (4-6)', str(medium), f'{medium/total*100:.1f}%', 
         'Moderate threat - should be monitored'],
        [f'🟢 Low (0-3)', str(low), f'{low/total*100:.1f}%', 
         'Minimal threat - routine events']
    ]
    
    table = Table(data, colWidths=[1.5*inch, 1*inch, 1*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['danger'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor(COLORS['border'])),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (1, 1), (0, 1), colors.HexColor('#fee2e2')),
        ('BACKGROUND', (1, 2), (0, 2), colors.HexColor('#ffedd5')),
        ('BACKGROUND', (1, 3), (0, 3), colors.HexColor('#fef9c3')),
        ('BACKGROUND', (1, 4), (0, 4), colors.HexColor('#dcfce7')),
    ]))
    story.append(table)

def build_mitigation_section(story, styles, df):
    """Build detailed mitigation section"""
    story.append(PageBreak())
    story.append(Paragraph("6. Detailed Attack Mitigation Guide", styles['SectionHeader']))
    
    story.append(Paragraph(
        "This section provides comprehensive mitigation strategies for each attack type detected "
        "in your honeypot. Each guide includes a detailed explanation, potential impacts, and "
        "step-by-step remediation instructions.",
        styles['ReportBody']
    ))
    
    story.append(Spacer(1, 0.3 * inch))
    
    if 'attack_type' not in df.columns:
        return
    
    attack_types_present = df['attack_type'].value_counts().index.tolist()
    
    for idx, attack_type in enumerate(attack_types_present, 1):
        if attack_type not in MITIGATION_GUIDES:
            continue
            
        guide = MITIGATION_GUIDES[attack_type]
        
        story.append(PageBreak())
        story.append(Paragraph(
            f"6.{idx} {attack_type} ({guide['severity']})",
            styles['SubsectionHeader']
        ))
        
        # Description
        story.append(Paragraph("<b>Description:</b>", styles['ReportBodyLeft']))
        story.append(Paragraph(guide['description'].strip(), styles['ReportBody']))
        
        # Statistics
        attack_df = df[df['attack_type'] == attack_type]
        stats_data = [
            ['Metric', 'Value'],
            ['Total Events', str(len(attack_df))],
            ['Percentage of All Attacks', f"{len(attack_df)/len(df)*100:.1f}%"],
            ['Average Risk Score', f"{attack_df['risk_score'].mean():.1f}"],
            ['Unique Attackers', str(attack_df['ip'].nunique())],
            ['Highest Single IP Count', str(attack_df['ip'].value_counts().iloc[0]) if len(attack_df) > 0 else "N/A"]
        ]
        
        stats_table = Table(stats_data, colWidths=[2*inch, 2.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['secondary'])),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor(COLORS['border'])),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(stats_table)
        
        story.append(Spacer(1, 0.2 * inch))
        
        # Mitigation Steps
        story.append(Paragraph("<b>Mitigation Steps:</b>", styles['ReportBodyLeft']))
        story.append(Spacer(1, 0.1 * inch))
        
        for step_num, (title, description) in enumerate(guide['steps'], 1):
            # Escape any special characters and use proper formatting  
            clean_title = str(title).replace('<', '<').replace('>', '>')
            
            # Handle multi-line descriptions by splitting into sentences
            desc_text = str(description)
            
            # Use separate paragraphs instead of <br/>
            story.append(Paragraph(
                f"<b>{step_num}. {clean_title}</b>",
                styles['MitigationStep']
            ))
            story.append(Paragraph(
                desc_text,
                styles['ReportBodyLeft']
            ))

def build_recommendations(story, styles):
    """Build recommendations section"""
    story.append(PageBreak())
    story.append(Paragraph("7. Security Recommendations", styles['SectionHeader']))
    
    recommendations = [
        ("Immediate Actions", [
            "Block IP addresses with risk scores ≥ 8 that show persistent attack patterns",
            "Review and patch all identified vulnerabilities within 24-48 hours",
            "Enable enhanced logging for all critical system events",
            "Activate WAF rules for SQL injection, XSS, and command injection"
        ]),
        ("Short-term (1-4 weeks)", [
            "Implement multi-factor authentication for all administrative access",
            "Deploy comprehensive Web Application Firewall with updated rules",
            "Conduct penetration testing to identify additional vulnerabilities",
            "Review and strengthen password policies across all systems"
        ]),
        ("Medium-term (1-3 months)", [
            "Implement security information and event management (SIEM) system",
            "Conduct regular vulnerability assessments and penetration testing",
            "Develop and document incident response procedures",
            "Implement network segmentation to limit lateral movement"
        ]),
        ("Long-term (Ongoing)", [
            "Maintain regular security awareness training for all staff",
            "Keep all software, libraries, and dependencies updated",
            "Conduct periodic security audits and code reviews",
            "Participate in threat intelligence sharing communities"
        ])
    ]
    
    for category, items in recommendations:
        story.append(Paragraph(category, styles['SubsectionHeader']))
        
        for item in items:
            story.append(Paragraph(f"• {item}", styles['ReportBodyLeft']))
        
        story.append(Spacer(1, 0.15 * inch))

def build_appendix(story, styles):
    """Build appendix with document information"""
    story.append(PageBreak())
    story.append(Paragraph("8. Appendix: Document Information", styles['SectionHeader']))
    
    info_data = [
        ['Property', 'Value'],
        ['Document Title', 'Cognitive Honeypot Security Analysis Report'],
        ['Version', '1.0'],
        ['Classification', 'Confidential'],
        ['Report Period', 'Since Honeypot Deployment'],
        ['Generated By', 'Cognitive Honeypot AI Security System'],
        ['Generation Date', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Total Pages', 'This document'],
    ]
    
    info_table = Table(info_data, colWidths=[1.8*inch, 3.5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(COLORS['primary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor(COLORS['border'])),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(info_table)
    
    story.append(Spacer(1, 0.5 * inch))
    
    story.append(Paragraph(
        "--- END OF REPORT ---",
        ParagraphStyle('End', parent=styles['Normal'], fontSize=12,
                     textColor=colors.HexColor(COLORS['muted']), alignment=TA_CENTER)
    ))

# ============================================================================
# MAIN GENERATOR
# ============================================================================

def generate_pdf(df, charts):
    """Generate the complete PDF report"""
    doc = SimpleDocTemplate(
        PDF_OUT,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=60,
        bottomMargin=60
    )
    
    styles = create_styles()
    story = []
    
    # Build all sections
    build_cover_page(story, styles, df, len(df))
    build_table_of_contents(story, styles)
    build_executive_summary(story, styles, df)
    build_top_ips(story, styles, df)
    build_visualizations(story, styles, charts)
    build_risk_assessment(story, styles, df)
    build_mitigation_section(story, styles, df)
    build_recommendations(story, styles)
    build_appendix(story, styles)
    
    # Build PDF with header/footer
    doc.build(story, onFirstPage=create_header, onLaterPages=create_header)

def main():
    print("🔒 Generating Professional Security Report...")
    print("=" * 50)
    
    # Load data
    print("📊 Loading log data...")
    df = load_logs()
    print(f"   Loaded {len(df)} events")
    
    # Generate charts
    print("📈 Generating visualizations...")
    charts = generate_charts(df)
    print(f"   Created {len(charts)} charts")
    
    # Generate PDF
    print("📄 Building PDF report...")
    generate_pdf(df, charts)
    
    print("=" * 50)
    print(f"✅ Report generated successfully!")
    print(f"   Output: {PDF_OUT}")
    print()
    print("Report Contents:")
    print("  • Cover Page with Executive Summary")
    print("  • Table of Contents")
    print("  • Attack Overview & Statistics")
    print("  • Top Attacking IP Addresses")
    print("  • Attack Visualizations (5 charts)")
    print("  • Risk Assessment Analysis")
    print("  • Detailed Mitigation Guide (per attack type)")
    print("  • Security Recommendations")
    print("  • Document Appendix")

if __name__ == "__main__":
    main()