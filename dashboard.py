import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Cognitive Honeypot Dashboard", layout="wide")

st.title("🛡️ Cognitive Honeypot Dashboard")

LOG_FILE = "data/logs.jsonl"

rows = []
try:
    with open(LOG_FILE, "r") as f:
        for line in f:
            rows.append(json.loads(line))
except FileNotFoundError:
    st.warning("No logs found yet. Run the honeypot and generate some traffic.")
    st.stop()

df = pd.DataFrame(rows)

st.metric("Total Events", len(df))

# Top IPs
if "ip" in df.columns:
    top_ips = df["ip"].value_counts().head(5)
    st.subheader("Top Attacking IPs")
    st.bar_chart(top_ips)

# Attack Types (Tags)
if "tags" in df.columns:
    all_tags = df["tags"].explode()
    st.subheader("Attack Types")
    st.bar_chart(all_tags.value_counts())

# Risk Score Distribution
if "risk_score" in df.columns:
    st.subheader("Risk Score Distribution")
    st.bar_chart(df["risk_score"].value_counts())

# 🧠 AI Anomaly Detection Section
if "ai_flag" in df.columns:
    st.subheader("AI Anomaly Detection")
    st.bar_chart(df["ai_flag"].value_counts())
    
# 🧠 AI Classifier Section
if "ai_attack_type" in df.columns:
    st.subheader("AI Attack Classification")
    st.bar_chart(df["ai_attack_type"].value_counts())
    
# Raw Logs Table
st.subheader("Raw Logs")
st.dataframe(df.tail(50))