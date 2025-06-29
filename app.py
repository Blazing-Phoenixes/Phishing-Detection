# app.py — Expert Flask Phishing Detection App
from flask import Flask, render_template, request
import pickle
import re
import numpy as np
import sqlite3
from datetime import datetime
import os

# --- Flask App Setup ---
app = Flask(__name__)

# --- Load ML Model ---
MODEL_PATH = "phishing_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# --- SQLite3 Setup ---
DB_NAME = "phishing_results.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Create results table if not exists
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            prediction TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- Feature Extraction ---
def extract_features(url: str) -> np.ndarray:
    return np.array([
        len(url),                                       # Length of URL
        1 if "@" in url else 0,                         # '@' in URL
        1 if url.startswith("https") else 0,            # HTTPS used
        1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0,  # IP in URL
        url.count('.')                                  # Count of dots
    ]).reshape(1, -1)

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    url = ""
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if not url:
            prediction = "Please enter a URL."
        else:
            features = extract_features(url)
            result = model.predict(features)[0]
            label = "Phishing" if result == 1 else "Legitimate"

            # Save result to database
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO results (url, prediction, timestamp) VALUES (?, ?, ?)",
                (url, label, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            conn.close()
            prediction = label
    return render_template("index.html", prediction=prediction, url=url)

@app.route("/logs")
def logs():
    conn = get_db_connection()
    results = conn.execute("SELECT * FROM results ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("logs.html", data=results)

# --- Run Server ---
if __name__ == "__main__":
    app.run(debug=True)