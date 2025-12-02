Using Pyton(FLASK)
This is a CRUD-based Employee Management System built using Python Flask.
It provides RESTful APIs and a web-based frontend to add, view, update, search, and delete employee records.
Employee data is stored in a JSON file.

Technologies Used
Python
Flask
Flask-CORS
HTML, CSS, JavaScript
REST API

Structure 
employee_backend/
├── app/
│   ├── flask_app.py
│   ├── employees.json
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
└── venv/

How to run
# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install flask flask-cors

# Run Flask server
python flask_app.py

Open Browser
http://127.0.0.1:5000


