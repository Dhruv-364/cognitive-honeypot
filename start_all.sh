#!/bin/bash

echo "🚀 Starting Cognitive Honeypot Platform..."

# Go to project root (use absolute path)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Start Python Web Honeypot
echo "🛡️ Starting Web Honeypot..."
osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR' && source venv/bin/activate && python web_honeypot.py\""

# Start SSH Honeypot (optional)
echo "🔐 Starting SSH Honeypot..."
osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR' && source venv/bin/activate && python ssh_honeypot.py\""

# Start UI Backend
echo "🧠 Starting UI Backend..."
osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR/ui-backend' && npm start\""

# Start React Frontend
echo "🎨 Starting Dashboard UI..."
osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR/ui-frontend' && npm start\""

# Start Attack Simulator
echo "🔥 Starting Attack Simulator..."
osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR' && source venv/bin/activate && python attack_simulator.py\""

echo "✅ All services launched!"
echo "🌐 Dashboard: http://localhost:3000"
echo "🛡️ Honeypot: http://127.0.0.1:5000"
echo "🔥 Attack Simulator: Running (auto-generating attacks)"

