from flask import Flask, request, render_template_string
import pickle
import re
import numpy as np
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# --- Load Model ---
MODEL_PATH = "phishing_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# --- SQLite Setup ---
DB_NAME = "phishing_results.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

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
        len(url),
        1 if "@" in url else 0,
        1 if url.startswith("https") else 0,
        1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0,
        url.count('.')
    ]).reshape(1, -1)

# --- Templates with Bootstrap ---
INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Phishing Detection</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
  <div class="container py-5">
    <h1 class="text-center mb-4">Phishing URL Detection</h1>
    <form method="POST" class="row justify-content-center">
      <div class="col-md-8 mb-3">
        <input type="text" name="url" class="form-control form-control-lg" placeholder="Enter a URL..." value="{{ url }}">
      </div>
      <div class="col-auto">
        <button type="submit" class="btn btn-primary btn-lg">Check</button>
      </div>
    </form>

    {% if prediction %}
      <div class="text-center mt-4">
        <div class="alert {% if prediction == 'Phishing' %}alert-danger{% else %}alert-success{% endif %} fs-5">
          <strong>{{ url }}</strong> is <strong>{{ prediction }}</strong>
        </div>
      </div>
    {% endif %}

    <div class="text-center mt-4">
      <a href="/logs" class="btn btn-outline-secondary">View Logs</a>
    </div>
  </div>
</body>
</html>
'''

LOGS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Detection Logs</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
  <div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Detection Logs</h2>
      <a href="/" class="btn btn-outline-primary">← Back to Home</a>
    </div>
    <div class="table-responsive">
      <table class="table table-bordered table-striped table-hover text-center align-middle">
        <thead class="table-primary">
          <tr>
            <th>ID</th>
            <th>URL</th>
            <th>Prediction</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {% for row in data %}
            <tr>
              <td>{{ row['id'] }}</td>
              <td class="text-break">{{ row['url'] }}</td>
              <td>
                <span class="badge {% if row['prediction'] == 'Phishing' %}bg-danger{% else %}bg-success{% endif %}">
                  {{ row['prediction'] }}
                </span>
              </td>
              <td>{{ row['timestamp'] }}</td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
'''

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    url = ""
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            features = extract_features(url)
            result = model.predict(features)[0]
            label = "Phishing" if result == 1 else "Legitimate"

            conn = get_db_connection()
            conn.execute(
                "INSERT INTO results (url, prediction, timestamp) VALUES (?, ?, ?)",
                (url, label, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
            conn.close()

            prediction = label
        else:
            prediction = "Phishing"  # Optional default warning

    return render_template_string(INDEX_TEMPLATE, prediction=prediction, url=url)

@app.route("/logs")
def logs():
    conn = get_db_connection()
    results = conn.execute("SELECT * FROM results ORDER BY id DESC").fetchall()
    conn.close()
    return render_template_string(LOGS_TEMPLATE, data=results)

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)