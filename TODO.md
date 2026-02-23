# Cloud Deployment TODO

## Tasks
- [x] Update frontend API URLs in ui-frontend/src/App.js
- [x] Update attack_simulator.py BASE_URL
- [x] Update generate_attacks.py BASE_URL
- [ ] Stage changes with git add
- [ ] Commit changes
- [ ] Push to repository

## URLs Updated ✓
- Frontend: http://localhost:4000 → https://cognitive-honeypot-1.onrender.com
- Attack Simulators: http://127.0.0.1:5000 → https://cognitive-honeypot-mxsf.onrender.com

## Summary of Changes

### 1. ui-frontend/src/App.js
Updated 4 API endpoints:
- `axios.get("http://localhost:4000/api/stats")` → `axios.get("https://cognitive-honeypot-1.onrender.com/api/stats")`
- `axios.get("http://localhost:4000/api/logs")` → `axios.get("https://cognitive-honeypot-1.onrender.com/api/logs")`
- `axios.get("http://localhost:4000/api/generate-report")` → `axios.get("https://cognitive-honeypot-1.onrender.com/api/generate-report")`
- `axios.get("http://localhost:4000/api/download-report")` → `axios.get("https://cognitive-honeypot-1.onrender.com/api/download-report")`

### 2. attack_simulator.py
- `BASE_URL = "http://127.0.0.1:5000"` → `BASE_URL = "https://cognitive-honeypot-mxsf.onrender.com"`

### 3. generate_attacks.py
- `BASE_URL = "http://127.0.0.1:5000"` → `BASE_URL = "https://cognitive-honeypot-mxsf.onrender.com"`

## Next Steps
Run the following git commands:
```bash
git add ui-frontend/src/App.js attack_simulator.py generate_attacks.py TODO.md
git commit -m "Update frontend and attack simulators to use cloud backend URLs"
git push
```
