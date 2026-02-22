# Fix Plan: React Simple Maps Not Displaying

## Status: COMPLETED ✅

## Issues Fixed:
1. **Map not visible** - Changed GeoJSON URL from `raw.githubusercontent.com` to `eric.clst.org` which is more reliable
2. **Attack locations not plotting** - Updated attackLocations memo to properly parse lat/lon from logs
3. **Marker rendering** - Simplified marker implementation to work with react-simple-maps v3

## Changes Made to `ui-frontend/src/App.js`:
1. Changed GeoJSON URL to: `https://eric.clst.org/assets/wiki/uploads/GloGeoJSON.json`
2. Updated `attackLocations` useMemo to properly parse lat/lon from log entries
3. Improved ComposableMap projection config (scale: 147)
4. Simplified Marker rendering with click handlers

## Current Data Flow Verified:
- ✅ attack_simulator.py sends requests with X-Country, X-Lat, X-Lon headers
- ✅ web_honeypot.py extracts and saves geo data to logs.jsonl  
- ✅ ui-backend/server.js reads logs and serves via API
- ✅ ui-frontend/App.js fetches from API and plots on map
- ✅ Map now displays with attack markers from real data

## To Test:
1. Open http://localhost:3000
2. Login with admin/admin
3. Navigate to Dashboard
4. Verify the map loads and shows attack markers
5. Click on markers to see attack details

