import React, { useEffect, useMemo, useState, useCallback } from "react";
import axios from "axios";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, LineChart, Line, PieChart, Pie, Cell
} from "recharts";
import { ComposableMap, Geographies, Geography, Marker } from "react-simple-maps";

// ==================== UI COMPONENTS ====================

function Card({ children, className = "" }) {
  return (
    <div className={`bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 ${className} transition-all duration-300 hover:shadow-xl`}>
      {children}
    </div>
  );
}

function StatCard({ title, value, accent, icon }) {
  return (
    <div className="rounded-2xl p-6 shadow-lg border border-gray-200 dark:border-gray-700 bg-gradient-to-br from-white to-gray-50 dark:from-gray-800 dark:to-gray-900 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl cursor-default">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">{title}</p>
          <p className={`text-4xl font-bold mt-2 ${accent}`}>{value}</p>
        </div>
        <div className={`text-4xl opacity-80 ${accent}`}>{icon}</div>
      </div>
    </div>
  );
}

function SeverityBadge({ risk }) {
  let color = "bg-green-500";
  let label = "Low";

  if (risk >= 6) {
    color = "bg-red-500";
    label = "High";
  } else if (risk >= 3) {
    color = "bg-orange-400";
    label = "Medium";
  }

  return (
    <span className={`px-3 py-1 text-xs rounded-full text-white font-medium ${color} shadow-sm`}>
      {label}
    </span>
  );
}

// Toast Notification Component
function Toast({ message, type, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);

  const colors = {
    success: "bg-green-500",
    error: "bg-red-500",
    info: "bg-blue-500"
  };

  return (
    <div className={`fixed top-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-xl z-50 animate-slide-in flex items-center gap-2`}>
      <span>{message}</span>
      <button onClick={onClose} className="ml-2 opacity-80 hover:opacity-100">×</button>
    </div>
  );
}

// Loading Skeleton
function Skeleton({ className }) {
  return (
    <div className={`animate-pulse bg-gray-300 dark:bg-gray-700 rounded ${className}`} />
  );
}

// ==================== LOGIN ====================

function Login({ onLogin }) {
  const [user, setUser] = useState("");
  const [pass, setPass] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async () => {
    if (!user || !pass) {
      setError("Please enter username and password");
      return;
    }
    
    setLoading(true);
    setError("");

    // Simulate network delay for better UX
    await new Promise(resolve => setTimeout(resolve, 500));

    if (user === "admin" && pass === "admin") {
      onLogin("admin");
    } else if (user === "viewer" && pass === "viewer") {
      onLogin("viewer");
    } else {
      setError("Invalid credentials. Use admin/admin or viewer/viewer");
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleLogin();
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-gray-900 to-slate-800 text-white relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>
      
      <div className="relative z-10 bg-gray-800/80 backdrop-blur-xl p-8 rounded-3xl shadow-2xl w-96 border border-gray-700/50">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mb-4 shadow-lg">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Cognitive Honeypot
          </h1>
          <p className="text-gray-400 text-sm mt-2">Security Operations Center</p>
        </div>
        
        <input 
          className="w-full mb-4 p-4 rounded-xl bg-gray-900/50 border border-gray-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all outline-none" 
          placeholder="Username" 
          value={user} 
          onChange={e => setUser(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <input 
          className="w-full mb-4 p-4 rounded-xl bg-gray-900/50 border border-gray-700 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all outline-none" 
          placeholder="Password" 
          type="password" 
          value={pass} 
          onChange={e => setPass(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        
        {error && (
          <div className="mb-4 p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-400 text-sm">
            {error}
          </div>
        )}
        
        <button 
          onClick={handleLogin} 
          disabled={loading}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 py-3 rounded-xl font-semibold transition-all hover:shadow-lg hover:shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Authenticating...
            </>
          ) : (
            "Sign In"
          )}
        </button>
        
        <div className="mt-6 text-center text-gray-500 text-xs">
          <p>Demo credentials:</p>
          <p className="mt-1">admin / admin | viewer / viewer</p>
        </div>
      </div>
    </div>
  );
}

// ==================== SIDEBAR ====================

const navItems = [
  { key: "DASHBOARD", label: "Dashboard", icon: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
    </svg>
  )},
  { key: "LOGS", label: "Attack Logs", icon: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  )},
  { key: "REPORTS", label: "Reports", icon: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  )},
  { key: "SETTINGS", label: "Settings", icon: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  )},
];

// ==================== DASHBOARD ====================

function Dashboard({ role, onLogout }) {
  // Demo attack locations for the map
  const demoAttackLocations = [
    { name: "India", coords: [78.9629, 20.5937], count: 120 },
    { name: "USA", coords: [-95.7129, 37.0902], count: 80 },
    { name: "Germany", coords: [10.4515, 51.1657], count: 45 },
    { name: "Russia", coords: [105.3188, 61.5240], count: 60 },
    { name: "China", coords: [104.1954, 35.8617], count: 90 },
  ];

  // Map zoom state
  const [mapZoom, setMapZoom] = useState(100);
  const [mapCenter, setMapCenter] = useState([0, 20]);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState(null);

  const handleZoomIn = () => {
    setMapZoom(prev => Math.min(prev + 30, 250));
  };

  const handleZoomOut = () => {
    setMapZoom(prev => Math.max(prev - 30, 50));
  };

  const handleMouseDown = (e) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX, y: e.clientY });
  };

  const handleMouseMove = (e) => {
    if (!isDragging || !dragStart) return;
    
    const deltaX = (e.clientX - dragStart.x) * 0.5;
    const deltaY = (e.clientY - dragStart.y) * 0.5;
    
    setMapCenter(prev => [
      prev[0] - deltaX,
      prev[1] + deltaY
    ]);
    setDragStart({ x: e.clientX, y: e.clientY });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    setDragStart(null);
  };

  const [stats, setStats] = useState({ total: 0, byType: {} });
  const [logs, setLogs] = useState([]);
  const [search, setSearch] = useState("");
  const [view, setView] = useState("DASHBOARD");
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);
  const [dark, setDark] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('theme') === 'dark' || document.documentElement.classList.contains("dark");
    }
    return true;
  });

  // Save theme preference
  useEffect(() => {
    localStorage.setItem('theme', dark ? 'dark' : 'light');
    if (dark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [dark]);

  const toggleTheme = () => setDark(!dark);

  const showToast = useCallback((message, type = "info") => {
    setToast({ message, type });
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, logsRes] = await Promise.all([
        axios.get("http://localhost:4000/api/stats"),
        axios.get("http://localhost:4000/api/logs")
      ]);
      setStats(statsRes.data);
      setLogs(logsRes.data);
      setLoading(false);
    } catch (err) {
      console.error("Failed to fetch data:", err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    if (!autoRefresh) return;
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, [autoRefresh]);

  const chartData = Object.entries(stats.byType || {}).map(([name, value]) => ({ name, value }));

  const timeSeries = useMemo(() => {
    const map = {};
    logs.forEach(l => {
      const t = (l.time || "").slice(0, 13);
      if (!t) return;
      map[t] = (map[t] || 0) + 1;
    });
    return Object.entries(map).sort((a, b) => a[0].localeCompare(b[0])).map(([time, count]) => ({ time, count }));
  }, [logs]);

  // Calculate attack locations from logs
  const attackLocations = useMemo(() => {
    if (logs && logs.length > 0) {
      const locationMap = {};
      logs.forEach(l => {
        const lat = parseFloat(l.lat) || parseFloat(l.latitude) || 0;
        const lon = parseFloat(l.lon) || parseFloat(l.longitude) || 0;
        if (lat !== 0 && lon !== 0) {
          const key = `${lat},${lon}`;
          if (!locationMap[key]) {
            locationMap[key] = { lat, lon, country: l.country || "Unknown", count: 0 };
          }
          locationMap[key].count++;
        }
      });
      
      const locations = Object.values(locationMap);
      if (locations.length > 0) {
        return locations;
      }
    }
    return null;
  }, [logs]);

  const [selectedLocation, setSelectedLocation] = useState(null);

  const exportCSV = () => {
    const csv = [
      ["time", "ip", "path", "risk", "tags"].join(","),
      ...logs.map(l => [l.time, l.ip, l.path, l.risk_score, (l.tags || []).join("|")].join(","))
    ].join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "honeypot_logs.csv";
    a.click();
    URL.revokeObjectURL(url);
    showToast("CSV exported successfully!", "success");
  };

  const generatePDF = async () => {
    try {
      showToast("Generating PDF report...", "info");
      await axios.get("http://localhost:4000/api/generate-report");
      const response = await axios.get("http://localhost:4000/api/download-report", {
        responseType: "blob"
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "honeypot_report.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      showToast("PDF report downloaded!", "success");
    } catch (e) {
      showToast("Failed to generate report", "error");
    }
  };

  // Filtered logs
  const filteredLogs = logs.filter(l => 
    `${l.ip} ${l.path} ${l.tags}`.toLowerCase().includes(search.toLowerCase())
  ).slice(-100).reverse();

  // COLORS for charts
  const COLORS = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899'];

  return (
    <div className="min-h-screen flex bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      {/* Toast Notification */}
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
      
      {/* Sidebar */}
      <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 p-4 flex flex-col">
        <div className="mb-8">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <span className="text-2xl">🛡️</span>
            <span className="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">SOC Panel</span>
          </h2>
        </div>
        
        <nav className="flex-1">
          {navItems.map(item => (
            <div
              key={item.key}
              onClick={() => setView(item.key)}
              className={`cursor-pointer p-3 rounded-xl mb-2 flex items-center gap-3 transition-all duration-200 ${
                view === item.key 
                  ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg shadow-blue-500/25" 
                  : "hover:bg-gray-200 dark:hover:bg-gray-700"
              }`}
            >
              {item.icon}
              <span className="font-medium">{item.label}</span>
            </div>
          ))}
        </nav>

        {/* User Info */}
        <div className="border-t border-gray-200 dark:border-gray-700 pt-4 mt-4">
          <div className="flex items-center gap-3 p-3 rounded-xl bg-gray-50 dark:bg-gray-700/50">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold">
              {role?.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-medium truncate">{role}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400 capitalize">{role} Access</p>
            </div>
            <button 
              onClick={onLogout}
              className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              title="Logout"
            >
              <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8 overflow-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold">
              {view === "DASHBOARD" && "Security Dashboard"}
              {view === "LOGS" && "Attack Logs"}
              {view === "REPORTS" && "Reports"}
              {view === "SETTINGS" && "Settings"}
            </h1>
            <p className="text-gray-500 dark:text-gray-400 mt-1">
              {view === "DASHBOARD" && "Real-time threat monitoring and analytics"}
              {view === "LOGS" && "Browse and search through attack logs"}
              {view === "REPORTS" && "Export and generate security reports"}
              {view === "SETTINGS" && "Configure dashboard preferences"}
            </p>
          </div>
          <div className="flex gap-3">
            <button 
              onClick={() => setAutoRefresh(a => !a)} 
              className={`px-4 py-2 rounded-xl font-medium transition-all ${
                autoRefresh 
                  ? "bg-green-500 text-white hover:bg-green-600" 
                  : "bg-gray-300 dark:bg-gray-700 hover:bg-gray-400"
              }`}
            >
              {autoRefresh ? "🔴 Live" : "⏸️ Paused"}
            </button>
            <button 
              onClick={toggleTheme} 
              className="px-4 py-2 rounded-xl bg-gray-300 dark:bg-gray-700 hover:bg-gray-400 dark:hover:bg-gray-600 transition-all flex items-center gap-2"
            >
              {dark ? (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                  Light
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
                  Dark
                </>
              )}
            </button>
          </div>
        </div>

        {/* Views */}
        {view === "DASHBOARD" && (
          <>
            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {loading ? (
                <>
                  <Skeleton className="h-32" />
                  <Skeleton className="h-32" />
                  <Skeleton className="h-32" />
                </>
              ) : (
                <>
                  <StatCard title="Total Attacks" value={stats.total} accent="text-red-500" icon="⚠️" />
                  <StatCard title="Attack Types" value={Object.keys(stats.byType || {}).length} accent="text-blue-500" icon="🔍" />
                  <StatCard title="Log Entries" value={logs.length} accent="text-green-500" icon="📋" />
                </>
              )}
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <Card>
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                  Attacks Over Time
                </h2>
                {loading ? (
                  <Skeleton className="h-64" />
                ) : (
                  <ResponsiveContainer width="100%" height={250}>
                    <LineChart data={timeSeries}>
                      <defs>
                        <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                      <XAxis dataKey="time" hide />
                      <YAxis />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: dark ? '#1f2937' : '#fff', 
                          border: 'none', 
                          borderRadius: '8px',
                          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                        }}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="count" 
                        stroke="#ef4444" 
                        strokeWidth={3}
                        dot={{ fill: '#ef4444', strokeWidth: 2, r: 4 }}
                        activeDot={{ r: 6, fill: '#ef4444' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                )}
              </Card>

              <Card>
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                  Attack Types Distribution
                </h2>
                {loading ? (
                  <Skeleton className="h-64" />
                ) : chartData.length > 0 ? (
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie
                        data={chartData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={90}
                        paddingAngle={2}
                        dataKey="value"
                      >
                        {chartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: dark ? '#1f2937' : '#fff', 
                          border: 'none', 
                          borderRadius: '8px',
                          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                        }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-64 flex items-center justify-center text-gray-500">
                    No attack data available
                  </div>
                )}
              </Card>
            </div>

            {/* Bar Chart */}
            <Card className="mb-8">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                Attack Categories
              </h2>
              {loading ? (
                <Skeleton className="h-64" />
              ) : (
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: dark ? '#1f2937' : '#fff', 
                        border: 'none', 
                        borderRadius: '8px',
                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                      }}
                    />
                    <Bar dataKey="value" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              )}
            </Card>

            {/* Map */}
            <Card>
              <h2 className="text-xl font-semibold mb-2">🌍 Global Attack Map</h2>
              <p className="text-sm text-gray-400 mb-4">
                Click on a marker to see attack count
              </p>

              <div 
                className="h-[360px] w-full overflow-hidden rounded-lg relative"
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                style={{ cursor: isDragging ? 'grabbing' : 'grab' }}
              >
                {/* Zoom Controls */}
                <div className="absolute bottom-3 right-3 z-10 flex flex-col gap-1">
                  <button 
                    onClick={handleZoomIn}
                    className="w-8 h-8 bg-gray-800 hover:bg-gray-700 text-white rounded flex items-center justify-center transition-colors"
                    title="Zoom In"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v12m6-6H6" />
                    </svg>
                  </button>
                  <button 
                    onClick={handleZoomOut}
                    className="w-8 h-8 bg-gray-800 hover:bg-gray-700 text-white rounded flex items-center justify-center transition-colors"
                    title="Zoom Out"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 12H6" />
                    </svg>
                  </button>
                </div>
                
                <ComposableMap 
                  projection="geoMercator"
                  projectionConfig={{
                    scale: mapZoom,
                    center: mapCenter
                  }}
                  width={800}
                  height={360}
                  style={{ width: "100%", height: "100%" }}
                >
                  <Geographies geography="/world.geojson">
                    {({ geographies, error, loading: geoLoading }) => {
                      if (error) {
                        console.error("Map error:", error);
                        return (
                          <text x="50%" y="50%" textAnchor="middle" fill="#6b7280" fontSize="14">
                            Failed to load map
                          </text>
                        );
                      }
                      if (geoLoading) {
                        return (
                          <text x="50%" y="50%" textAnchor="middle" fill="#6b7280" fontSize="14">
                            Loading map...

                          </text>
                        );
                      }
                      return geographies.map((geo) => (
                        <Geography
                          key={geo.rsmKey}
                          geography={geo}
                          fill="#374151"
                          stroke="#9ca3af"
                          strokeWidth={0.75}
                          style={{
                            default: { outline: "none" },
                            hover: { fill: "#4b5563", outline: "none" },
                            pressed: { outline: "none" },
                          }}
                        />
                      ));
                    }}
                  </Geographies>

                  {attackLocations && attackLocations.length > 0 ? (
                    attackLocations.map((loc, i) => (
                      <Marker 
                        key={i} 
                        coordinates={[loc.lon, loc.lat]}
                        onClick={() => setSelectedLocation(loc)}
                        style={{ cursor: "pointer" }}
                      >
                        <circle
                          r={Math.min(8, 3 + loc.count / 30)}
                          fill="#ef4444"
                          stroke="#fff"
                          strokeWidth={1.5}
                          opacity={0.9}
                        />
                      </Marker>
                    ))
                  ) : (
                    demoAttackLocations.map((loc, i) => (
                      <Marker 
                        key={i} 
                        coordinates={loc.coords}
                        onClick={() => setSelectedLocation({ country: loc.name, lat: loc.coords[1], lon: loc.coords[0], count: loc.count })}
                        style={{ cursor: "pointer" }}
                      >
                        <circle
                          r={Math.min(8, 3 + loc.count / 30)}
                          fill="#ef4444"
                          stroke="#fff"
                          strokeWidth={1.5}
                          opacity={0.9}
                        />
                      </Marker>
                    ))
                  )}
                </ComposableMap>
                
                {selectedLocation && (
                  <div className="absolute top-2 right-2 bg-black/80 text-white px-4 py-2 rounded-lg backdrop-blur-sm">
                    <p className="font-bold text-lg">{selectedLocation.country}</p>
                    <p className="text-sm text-gray-300">
                      {selectedLocation.count} attacks
                    </p>
                    <button 
                      onClick={() => setSelectedLocation(null)}
                      className="mt-1 text-xs text-gray-400 hover:text-white"
                    >
                      ✕ Close
                    </button>
                  </div>
                )}
              </div>
            </Card>
          </>
        )}

        {view === "LOGS" && (
          <Card>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Attack Logs</h2>
              <span className="text-sm text-gray-500">{filteredLogs.length} entries</span>
            </div>
            <div className="relative mb-4">
              <svg className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input 
                className="w-full p-3 pl-12 rounded-xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 outline-none transition-all" 
                placeholder="Search by IP, path, or tags..." 
                value={search} 
                onChange={e => setSearch(e.target.value)} 
              />
            </div>
            <div className="overflow-auto max-h-[500px] rounded-xl border border-gray-200 dark:border-gray-700">
              {loading ? (
                <div className="p-4 space-y-2">
                  {[...Array(5)].map((_, i) => <Skeleton key={i} className="h-12" />)}
                </div>
              ) : filteredLogs.length === 0 ? (
                <div className="p-8 text-center text-gray-500">
                  <svg className="w-12 h-12 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  No logs found
                </div>
              ) : (
                <table className="w-full text-sm">
                  <thead className="sticky top-0 bg-gray-100 dark:bg-gray-700">
                    <tr>
                      <th className="text-left p-4 font-semibold">Time</th>
                      <th className="text-left p-4 font-semibold">IP</th>
                      <th className="text-left p-4 font-semibold">Path</th>
                      <th className="text-left p-4 font-semibold">Risk</th>
                      <th className="text-left p-4 font-semibold">Severity</th>
                      <th className="text-left p-4 font-semibold">Tags</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredLogs.map((l, i) => (
                      <tr key={i} className="border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/40 transition-colors">
                        <td className="p-4 font-mono text-xs">{l.time}</td>
                        <td className="p-4 font-mono">{l.ip}</td>
                        <td className="p-4 max-w-xs truncate" title={l.path}>{l.path}</td>
                        <td className="p-4">
                          <span className={`font-bold ${
                            l.risk_score >= 6 ? 'text-red-500' : 
                            l.risk_score >= 3 ? 'text-orange-500' : 'text-green-500'
                          }`}>
                            {l.risk_score}
                          </span>
                        </td>
                        <td className="p-4"><SeverityBadge risk={l.risk_score} /></td>
                        <td className="p-4">
                          <div className="flex flex-wrap gap-1">
                            {(l.tags || []).map((tag, j) => (
                              <span key={j} className="px-2 py-0.5 bg-gray-200 dark:bg-gray-600 rounded text-xs">
                                {tag}
                              </span>
                            ))}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </Card>
        )}

        {view === "REPORTS" && (
          <Card>
            <h2 className="text-xl font-semibold mb-6">Export Reports</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="p-6 rounded-xl border-2 border-dashed border-gray-300 dark:border-gray-600 hover:border-green-500 transition-colors group">
                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="font-semibold mb-2">Export CSV</h3>
                  <p className="text-sm text-gray-500 mb-4">Download all attack logs as CSV</p>
                  <button 
                    onClick={exportCSV}
                    className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg transition-all hover:shadow-lg"
                  >
                    Download CSV
                  </button>
                </div>
              </div>
              
              <div className="p-6 rounded-xl border-2 border-dashed border-gray-300 dark:border-gray-600 hover:border-red-500 transition-colors group">
                <div className="text-center">
                  <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="font-semibold mb-2">Generate PDF Report</h3>
                  <p className="text-sm text-gray-500 mb-4">Create a comprehensive PDF analysis</p>
                  <button 
                    onClick={generatePDF}
                    className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg transition-all hover:shadow-lg"
                  >
                    Generate PDF
                  </button>
                </div>
              </div>
            </div>
          </Card>
        )}

        {view === "SETTINGS" && (
          <Card>
            <h2 className="text-xl font-semibold mb-6">Dashboard Settings</h2>
            <div className="space-y-6">
              <div className="flex items-center justify-between p-4 rounded-xl bg-gray-50 dark:bg-gray-700/50">
                <div>
                  <h3 className="font-medium">Auto Refresh</h3>
                  <p className="text-sm text-gray-500">Automatically refresh data every 5 seconds</p>
                </div>
                <button 
                  onClick={() => setAutoRefresh(a => !a)} 
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    autoRefresh ? 'bg-blue-600' : 'bg-gray-300 dark:bg-gray-600'
                  }`}
                >
                  <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    autoRefresh ? 'translate-x-6' : 'translate-x-1'
                  }`} />
                </button>
              </div>
              
              <div className="flex items-center justify-between p-4 rounded-xl bg-gray-50 dark:bg-gray-700/50">
                <div>
                  <h3 className="font-medium">Dark Mode</h3>
                  <p className="text-sm text-gray-500">Switch between light and dark themes</p>
                </div>
                <button 
                  onClick={toggleTheme} 
                  className="px-4 py-2 rounded-lg bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-500 transition-all"
                >
                  {dark ? 'Switch to Light' : 'Switch to Dark'}
                </button>
              </div>
              
              <div className="flex items-center justify-between p-4 rounded-xl bg-gray-50 dark:bg-gray-700/50">
                <div>
                  <h3 className="font-medium">Session</h3>
                  <p className="text-sm text-gray-500">Currently logged in as {role}</p>
                </div>
                <button 
                  onClick={onLogout}
                  className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-700 text-white transition-all"
                >
                  Logout
                </button>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}

// ==================== ROOT ====================

function App() {
  const [role, setRole] = useState(() => {
    // Check localStorage on initial load
    if (typeof window !== 'undefined') {
      return localStorage.getItem('userRole');
    }
    return null;
  });

  const handleLogin = (userRole) => {
    localStorage.setItem('userRole', userRole);
    setRole(userRole);
  };

  const handleLogout = () => {
    localStorage.removeItem('userRole');
    setRole(null);
  };

  if (!role) return <Login onLogin={handleLogin} />;
  return <Dashboard role={role} onLogout={handleLogout} />;
}

export default App;

