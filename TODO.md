# Cloud Deployment TODO

## Tasks
- [x] Update frontend API URLs in ui-frontend/src/App.js
- [x] Update attack_simulator.py BASE_URL
- [x] Update generate_attacks.py BASE_URL
- [x] Stage changes with git add
- [x] Commit changes
- [x] Push to repository
- [x] Verify cloud URLs on GitHub

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

## Status: ✅ COMPLETE - VERIFIED ON GITHUB

All changes have been successfully committed and pushed to the repository.

**Commit:** `b6f0bf3` - Update frontend to use cloud backend URL and attack simulators to use cloud honeypot

**Files Modified:**
- `ui-frontend/src/App.js` - Updated 4 API endpoints to use cloud backend
- `attack_simulator.py` - Updated BASE_URL to cloud honeypot
- `generate_attacks.py` - Updated BASE_URL to cloud honeypot

**Verified on GitHub:**
- ✅ Frontend API calls use https://cognitive-honeypot-1.onrender.com
- ✅ Attack simulator uses https://cognitive-honeypot-mxsf.onrender.com

**Cloud URLs:**
- Frontend: https://cognitive-honeypot.vercel.app
- Backend API: https://cognitive-honeypot-1.onrender.com
- Honeypot: https://cognitive-honeypot-mxsf.onrender.com

**Repository:** https://github.com/Dhruv-364/cognitive-honeypot
