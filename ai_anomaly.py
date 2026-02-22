import json
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

LOG_FILE = "data/logs.jsonl"

def load_logs():
    rows = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            rows.append(json.loads(line))
    return pd.DataFrame(rows)

def feature_engineering(df):
    # Simple numeric features
    df["path_len"] = df["path"].fillna("").apply(len)
    df["has_data"] = df.get("data", "").astype(str).apply(len)
    df["risk_score"] = df["risk_score"].fillna(0)

    features = df[["path_len", "has_data", "risk_score"]]
    return features.fillna(0)

def run_anomaly_detection():
    df = load_logs()
    if len(df) < 10:
        print("Not enough data yet for anomaly detection.")
        return

    X = feature_engineering(df)

    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(X)

    scores = model.decision_function(X)
    preds = model.predict(X)  # -1 = anomaly, 1 = normal

    df["ai_anomaly_score"] = scores
    df["ai_flag"] = ["Anomaly" if p == -1 else "Normal" for p in preds]

    # Save enriched logs
    with open(LOG_FILE, "w") as f:
        for _, row in df.iterrows():
            f.write(json.dumps(row.to_dict()) + "\n")

    print("✅ AI anomaly detection applied to logs.")

if __name__ == "__main__":
    run_anomaly_detection()