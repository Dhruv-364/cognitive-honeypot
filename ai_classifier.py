import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

LOG_FILE = "data/logs.jsonl"

def load_logs():
    rows = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            rows.append(json.loads(line))
    return pd.DataFrame(rows)

def feature_engineering(df):
    df["path_len"] = df["path"].fillna("").apply(len)
    df["data_len"] = df.get("data", "").astype(str).apply(len)
    df["risk_score"] = df["risk_score"].fillna(0)
    return df[["path_len", "data_len", "risk_score"]]

def generate_labels(df):
    # Use existing tags as weak labels (for demo/training)
    labels = []
    for tags in df.get("tags", []):
        if isinstance(tags, list):
            if "SQLi" in tags:
                labels.append("SQLi")
            elif "XSS" in tags:
                labels.append("XSS")
            elif "Bruteforce" in tags:
                labels.append("Bruteforce")
            elif "Scanner-Probe" in tags:
                labels.append("Scanner")
            else:
                labels.append("Normal")
        else:
            labels.append("Normal")
    return labels

def run_classifier():
    df = load_logs()
    if len(df) < 20:
        print("Not enough data yet for training classifier.")
        return

    X = feature_engineering(df)
    y = generate_labels(df)

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y_enc)

    preds = model.predict(X)
    pred_labels = le.inverse_transform(preds)

    df["ai_attack_type"] = pred_labels

    # Save back to log file
    with open(LOG_FILE, "w") as f:
        for _, row in df.iterrows():
            f.write(json.dumps(row.to_dict()) + "\n")

    print("✅ AI attack classification applied to logs.")

if __name__ == "__main__":
    run_classifier()