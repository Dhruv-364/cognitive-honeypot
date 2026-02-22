const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const { exec } = require("child_process");

const app = express();
app.use(cors());

// Absolute paths (robust)
const ROOT_DIR = path.join(__dirname, "..");
const DATA_DIR = path.join(ROOT_DIR, "data");
const LOG_FILE = path.join(DATA_DIR, "logs.jsonl");

// Change this if your generate_report.py outputs a different name
const REPORT_FILE = path.join(DATA_DIR, "report.pdf");
const REPORT_SCRIPT = path.join(ROOT_DIR, "generate_report.py");

// Helper: read logs safely (skip bad JSON lines)
function readLogs() {
  if (!fs.existsSync(LOG_FILE)) return [];

  const content = fs.readFileSync(LOG_FILE, "utf-8").trim();
  if (!content) return [];

  const lines = content.split("\n");
  const logs = [];

  for (const line of lines) {
    try {
      const obj = JSON.parse(line);
      logs.push(obj);
    } catch (err) {
      console.warn("⚠️ Skipping invalid log line");
    }
  }

  return logs;
}

// ------------------- API -------------------

// Logs endpoint
app.get("/api/logs", (req, res) => {
  try {
    const logs = readLogs();
    res.json(logs);
  } catch (err) {
    console.error("Error in /api/logs:", err);
    res.status(500).json({ error: "Failed to read logs" });
  }
});

// Stats endpoint
app.get("/api/stats", (req, res) => {
  try {
    const logs = readLogs();
    const total = logs.length;

    const byType = {};
    logs.forEach(l => {
      if (l.tags && l.tags.length > 0) {
        const t = l.tags[0];
        byType[t] = (byType[t] || 0) + 1;
      }
    });

    res.json({ total, byType });
  } catch (err) {
    console.error("Error in /api/stats:", err);
    res.status(500).json({ error: "Failed to compute stats" });
  }
});

// Generate PDF report
app.get("/api/generate-report", (req, res) => {
  // Absolute paths
  const ROOT = path.join(__dirname, "..");
  const SCRIPT = path.join(ROOT, "generate_report.py");
  
  // Use absolute path to Python venv
  const PYTHON = path.join(ROOT, "venv/bin/python");

  // Check if Python exists, fallback to system python
  const pythonCmd = fs.existsSync(PYTHON) ? PYTHON : "python3";

  const cmd = `"${pythonCmd}" "${SCRIPT}"`;

  console.log("📄 Running:", cmd);

  exec(cmd, { cwd: ROOT }, (err, stdout, stderr) => {
    if (err) {
      console.error("❌ Report generation error:", err);
      console.error("STDERR:", stderr);
      return res.status(500).send("Error generating report");
    }

    console.log(stdout);
    res.send("Report generated successfully");
  });
});

// Download latest report
app.get("/api/download-report", (req, res) => {
  if (!fs.existsSync(REPORT_FILE)) {
    return res.status(404).send("Report not found. Generate it first.");
  }

  res.download(REPORT_FILE, "honeypot_report.pdf");
});

// ------------------- START -------------------

app.listen(4000, () => {
  console.log("🚀 UI Backend running on http://localhost:4000");
  console.log("📄 Reading logs from:", LOG_FILE);
  console.log("📑 Report script:", REPORT_SCRIPT);
  console.log("📥 Report output:", REPORT_FILE);
});

