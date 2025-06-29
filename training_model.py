# train_model.py — create phishing_model.pkl
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Sample dummy training data
# Format: [url_length, has_@, has_https, has_ip, dot_count]
X = np.array([
    [75, 1, 0, 1, 5],
    [60, 0, 1, 0, 3],
    [120, 1, 0, 1, 6],
    [45, 0, 1, 0, 2],
    [85, 1, 1, 1, 7],
    [55, 0, 1, 0, 3],
])

# Labels: 1 = phishing, 0 = legitimate
y = np.array([1, 0, 1, 0, 1, 0])

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
with open("phishing_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ phishing_model.pkl created successfully!")