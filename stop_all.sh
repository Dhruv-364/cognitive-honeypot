#!/bin/bash

echo "🛑 Stopping Cognitive Honeypot Platform..."

# Kill Python processes (web_honeypot.py, ssh_honeypot.py, attack_simulator.py)
echo "🛡️ Stopping Python honeypot processes..."
pkill -f "python web_honeypot.py" 2>/dev/null && echo "✓ Web Honeypot stopped" || echo "✓ Web Honeypot not running"
pkill -f "python ssh_honeypot.py" 2>/dev/null && echo "✓ SSH Honeypot stopped" || echo "✓ SSH Honeypot not running"
pkill -f "python attack_simulator.py" 2>/dev/null && echo "✓ Attack Simulator stopped" || echo "✓ Attack Simulator not running"

# Kill Node/React processes
echo "🖥️ Stopping Node processes..."
pkill -f "node.*ui-backend" 2>/dev/null && echo "✓ UI Backend stopped" || echo "✓ UI Backend not running"
pkill -f "node.*ui-frontend" 2>/dev/null && echo "✓ React Frontend stopped" || echo "✓ React Frontend not running"

# Kill processes on specific ports
echo "🔌 Stopping services on specific ports..."

# Port 5000 (Flask web honeypot)
lsof -ti:5000 | xargs kill 2>/dev/null && echo "✓ Port 5000 freed" || echo "✓ Port 5000 not in use"

# Port 2222 (SSH honeypot)
lsof -ti:2222 | xargs kill 2>/dev/null && echo "✓ Port 2222 freed" || echo "✓ Port 2222 not in use"

# Port 4000 (UI Backend)
lsof -ti:4000 | xargs kill 2>/dev/null && echo "✓ Port 4000 freed" || echo "✓ Port 4000 not in use"

# Port 3000 (React Frontend)
lsof -ti:3000 | xargs kill 2>/dev/null && echo "✓ Port 3000 freed" || echo "✓ Port 3000 not in use"

echo "✅ All services stopped!"

