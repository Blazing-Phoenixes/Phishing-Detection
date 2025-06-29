# Phishing-Detection

 🔐 Phishing Website Detection System

A lightweight Flask web application to detect phishing websites using machine learning and URL feature extraction.


 ✅ Features
Real-time phishing prediction using trained model
Web interface built with Flask
Stores scan history in SQLite3
Highlights result as Phishing or Legitimate


🧰 Technologies Used
 Python 3.x
 Flask (Web Framework)
 Scikitlearn (Machine Learning)
 SQLite3 (Database)
 HTML/CSS/JS (Frontend)


 📁 Project Structure
```
├── app.py                   # Flask web app
├── train_model.py           # Model training script
├── phishing_model.pkl       # Trained ML model
├── phishing_results.db      # SQLite3 database
├── templates/
│   ├── index.html           # Main input page
│   └── logs.html            # Logs history page
└── README.md
```


 🔮 Future Enhancements
 WHOIS and domain age analysis
 Browser extension integration
 Admin panel and statistics
📃 License
This project is opensource and intended for educational use only.

