# Phishing-Detection

 🔐 Phishing Website Detection System

A lightweight Flask web application to detect phishing websites using machine learning and URL feature extraction.


 ✅ Features
1. Real-time phishing prediction using trained model
2. Web interface built with Flask
3. Stores scan history in SQLite3
4. Highlights result as Phishing or Legitimate


🧰 Technologies Used
1. Python 3.x
2. Flask (Web Framework)
3. Scikitlearn (Machine Learning)
4. SQLite3 (Database)
5. HTML/CSS/JS (Frontend)


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
1. WHOIS and domain age analysis
2. Browser extension integration
3. Admin panel and statistics

📃 License
This project is opensource and intended for educational use only.

