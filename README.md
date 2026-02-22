# 🛡️ Cognitive Honeypot - AI-Powered Security Operations Center

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/React-18+-61DAFB.svg" alt="React">
  <img src="https://img.shields.io/badge/Node.js-16+-339933.svg" alt="Node.js">
  <img src="https://img.shields.io/badge/Tailwind-CSS-38bdf8.svg" alt="Tailwind">
</p>

A comprehensive, intelligent honeypot system designed to detect, analyze, and visualize cyber attacks in real-time. The Cognitive Honeypot combines traditional honeypot techniques with AI-powered threat analysis to provide deep insights into attacker behaviors and attack patterns.

---

## 📋 Table of Contents

- [🌟 Features](#-features)
- [🏗️ Architecture](#-architecture)
- [🚀 Quick Start](#-quick-start)
- [📦 Prerequisites](#-prerequisites)
- [💻 Installation & Setup](#-installation--setup)
- [🔐 Credentials](#-credentials)
- [📊 Dashboard Features](#-dashboard-features)
- [🔧 Component Details](#-component-details)
- [📁 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 Features

### Core Features
- **🌐 Interactive Attack Map** - Real-time global visualization of attack origins with zoom, pan, and click-to-details functionality
- **📈 Attack Analytics** - Comprehensive charts showing attack trends, types distribution, and categories
- **🔍 Real-time Logs** - Live attack log viewer with search and filtering capabilities
- **📄 Report Generation** - Export attack data as CSV or generate detailed PDF reports
- **🔐 Secure Authentication** - Role-based access control (Admin/Viewer)

### AI-Powered Features
- **🤖 Anomaly Detection** - AI-based detection of unusual attack patterns
- **🧠 Threat Classification** - Automatic categorization of attack types using machine learning
- **💡 GenAI Analysis** - Intelligent insights and recommendations powered by generative AI

### Technical Features
- **🕷️ Web Honeypot** - Captures HTTP/HTTPS attack attempts
- **🔑 SSH Honeypot** - Monitors unauthorized SSH access attempts
- **⚡ Real-time Processing** - Instant logging and visualization of attacks
- **📊 Data Persistence** - JSON-based log storage with CSV export support

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Cognitive Honeypot                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │ Web Honeypot │    │ SSH Honeypot │    │   Attack     │   │
│  │  (Port 5000) │    │  (Port 2222) │    │  Simulator   │   │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘   │
│         │                   │                   │            │
│         └───────────────────┼───────────────────┘            │
│                             ▼                                 │
│                  ┌──────────────────┐                        │
│                  │   Data Storage   │                        │
│                  │  (logs.jsonl)    │                        │
│                  └────────┬─────────┘                        │
│                           │                                   │
│                           ▼                                   │
│                  ┌──────────────────┐                        │
│                  │   Backend API    │                        │
│                  │  (Port 4000)     │                        │
│                  └────────┬─────────┘                        │
│                           │                                   │
│                           ▼                                   │
│                  ┌──────────────────┐                        │
│                  │  React Frontend  │                        │
│                  │  (Port 3000)     │                        │
│                  └──────────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

The fastest way to get started:

```bash
# 1. Clone the repository
cd cognitive_honeypot

# 2. Start all services
./start_all.sh

# 3. Access the dashboard
# Open http://localhost:3000 in your browser
```

---

## 📦 Prerequisites

| Component | Version | Description |
|-----------|---------|-------------|
| Python | 3.9+ | Backend processing |
| Node.js | 16+ | Frontend & API server |
| npm | 8+ | Package management |

### Python Dependencies
- Flask (Web server)
- requests (HTTP requests)
- pandas (Data analysis)
- fpdf (PDF generation)
- scikit-learn (ML/AI)

### Node.js Dependencies
- React 18
- Express
- Axios
- Recharts
- React Simple Maps
- Tailwind CSS

---

## 💻 Installation & Setup

### Option 1: Automated Setup (Recommended)

```bash
# Make scripts executable
chmod +x start_all.sh
chmod +x stop_all.sh

# Start all components
./start_all.sh
```

### Option 2: Manual Setup

#### Step 1: Start the Backend API Server

```bash
cd cognitive_honeypot/ui-backend
npm install
npm start
```

#### Step 2: Start the Frontend

```bash
cd cognitive_honeypot/ui-frontend
npm install
npm start
```

#### Step 3: Run the Honeypot Services

```bash
# Terminal 1: Web Honeypot
python3 web_honeypot.py

# Terminal 2: SSH Honeypot  
python3 ssh_honeypot.py

# Terminal 3: Attack Simulator (for testing)
python3 attack_simulator.py
```

---

## 🔐 Credentials

| Role | Username | Password | Permissions |
|------|----------|----------|-------------|
| Admin | `admin` | `admin` | Full access to all features |
| Viewer | `viewer` | `viewer` | Read-only access |

---

## 📊 Dashboard Features

### 🏠 Dashboard View
- **Total Attacks Counter** - Real-time count of all attacks
- **Attack Types** - Number of distinct attack categories
- **Log Entries** - Total captured log entries
- **Attacks Over Time** - Line chart showing attack trends
- **Attack Distribution** - Pie chart of attack types
- **Attack Categories** - Bar chart of attack categories
- **Global Attack Map** - Interactive world map with attack origins

### 🗺️ Global Attack Map Features
- 🌍 Interactive world map visualization
- 🔴 Red markers showing attack origins
- ➕ Zoom in button
- ➖ Zoom out button  
- 🖱️ Click and drag to pan
- 👆 Click markers for attack details
- 📊 Real-time data from honeypot logs

### 📝 Attack Logs View
- 🔍 Searchable log entries
- 📋 Sortable columns
- 🏷️ Attack type tags
- ⚠️ Risk score indicators
- 📄 Detailed attack information

### 📈 Reports View
- 📥 Export to CSV
- 📑 Generate PDF reports
- 📊 Analytics summary

### ⚙️ Settings View
- 🔄 Auto-refresh toggle
- 🌓 Dark/Light mode
- 🚪 Logout functionality

---

## 🔧 Component Details

### Backend Components

| File | Description |
|------|-------------|
| `web_honeypot.py` | HTTP/HTTPS honeypot that captures web attacks |
| `ssh_honeypot.py` | SSH honeypot for monitoring brute force attempts |
| `attack_simulator.py` | Simulates various attack types for testing |
| `generate_report.py` | Generates PDF reports from attack data |
| `ai_classifier.py` | ML-based attack classification |
| `ai_anomaly.py` | Anomaly detection using AI |
| `genai_engine.py` | Generative AI for threat analysis |

### Frontend Components

| File | Description |
|------|-------------|
| `ui-backend/server.js` | Express API server |
| `ui-frontend/src/App.js` | Main React application |

---

## 📁 Project Structure

```
cognitive_honeypot/
├── ai_anomaly.py           # AI anomaly detection
├── ai_classifier.py        # ML attack classifier
├── attack_simulator.py      # Attack simulation tool
├── dashboard.py            # Dashboard backend
├── genai_engine.py        # GenAI integration
├── generate_attacks.py     # Attack generation
├── generate_report.py      # PDF report generator
├── ssh_honeypot.py        # SSH honeypot
├── web_honeypot.py        # Web honeypot
├── start_all.sh           # Start all services
├── stop_all.sh            # Stop all services
├── FIX_TODO.md           # Development notes
│
├── data/                  # Data directory
│   ├── logs.jsonl        # Attack logs (JSON Lines)
│   ├── ssh_logs.jsonl   # SSH honeypot logs
│   ├── report.csv        # Exported CSV data
│   └── charts/           # Chart data
│
├── ui-backend/            # Backend API
│   ├── server.js         # Express server
│   └── package.json
│
└── ui-frontend/          # React Frontend
    ├── public/
    │   └── world.geojson # World map data
    ├── src/
    │   └── App.js       # Main React app
    └── package.json
```

---

## 🚦 Running the Services

### Start Everything
```bash
./start_all.sh
```

### Stop Everything
```bash
./stop_all.sh
```

### Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main dashboard |
| Backend API | http://localhost:4000 | REST API |
| Web Honeypot | http://localhost:5000 | Captures web attacks |
| SSH Honeypot | localhost:2222 | SSH on port 2222 |

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/api/logs` | GET | Fetch all attack logs |
| `/api/stats` | GET | Get attack statistics |
| `/api/generate-report` | GET | Generate PDF report |
| `/api/download-report` | GET | Download generated PDF |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [React Simple Maps](https://www.react-simple-maps.org/) - For the interactive map component
- [Recharts](https://recharts.org/) - For beautiful charts
- [Tailwind CSS](https://tailwindcss.com/) - For styling
- [OpenStreetMap](https://www.openstreetmap.org/) - For map data

---

<p align="center">
  Made with ❤️ for cybersecurity research
</p>

