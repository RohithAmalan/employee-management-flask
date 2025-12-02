from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os

# Base directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  # allow frontend JS to call the API

# Store employees.json inside the app folder
DATA_FILE = os.path.join(BASE_DIR, "employees.json")


def load_employees():
    """Load employee data from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_employees(employees):
    """Save employee data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(employees, f, indent=2)


def get_next_id(employees):
    """Generate the next employee ID."""
    if not employees:
        return 1
    return max(emp["id"] for emp in employees) + 1


# ----------------- FRONTEND ROUTE ----------------- #

@app.route("/")
def index():
    """Serve the HTML frontend."""
    return render_template("index.html")


# ----------------- API ROUTES (REST) ----------------- #

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"message": "Flask Employee API is running"})


# CREATE employee
@app.route("/api/employees", methods=["POST"])
def create_employee():
    employees = load_employees()
    data = request.get_json() or {}

    # Basic required fields
    required_fields = ["name", "email", "phone"]
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            return jsonify({"error": f"'{field}' is required"}), 400

    # Phone validation: exactly 10 digits
    raw_phone = str(data.get("phone", "")).strip()
    phone_digits = "".join(ch for ch in raw_phone if ch.isdigit())
    if len(phone_digits) != 10:
        return jsonify({"error": "Phone number must be exactly 10 digits"}), 400

    new_employee = {
        "id": get_next_id(employees),
        "name": data["name"],
        "email": data["email"],
        "phone": phone_digits,
        "role": data.get("role", ""),
        "department": data.get("department", ""),
        "salary": data.get("salary", 0),
        "date_of_joining": data.get("date_of_joining", ""),
        "status": data.get("status", "Active"),
    }

    employees.append(new_employee)
    save_employees(employees)

    return jsonify(new_employee), 201


# READ all employees
@app.route("/api/employees", methods=["GET"])
def get_employees():
    employees = load_employees()
    return jsonify(employees), 200


# READ single employee
@app.route("/api/employees/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    employees = load_employees()
    for emp in employees:
        if emp["id"] == emp_id:
            return jsonify(emp), 200

    return jsonify({"error": "Employee not found"}), 404


# UPDATE employee
@app.route("/api/employees/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    employees = load_employees()
    data = request.get_json() or {}

    for emp in employees:
        if emp["id"] == emp_id:
            # Optional: validate phone if provided
            if "phone" in data:
                raw_phone = str(data.get("phone", "")).strip()
                phone_digits = "".join(ch for ch in raw_phone if ch.isdigit())
                if len(phone_digits) != 10:
                    return jsonify({"error": "Phone number must be exactly 10 digits"}), 400
                emp["phone"] = phone_digits

            emp["name"] = data.get("name", emp["name"])
            emp["email"] = data.get("email", emp["email"])
            emp["role"] = data.get("role", emp.get("role", ""))
            emp["department"] = data.get("department", emp.get("department", ""))
            emp["salary"] = data.get("salary", emp.get("salary", 0))
            emp["date_of_joining"] = data.get(
                "date_of_joining", emp.get("date_of_joining", "")
            )
            emp["status"] = data.get("status", emp.get("status", "Active"))

            save_employees(employees)
            return jsonify(emp), 200

    return jsonify({"error": "Employee not found"}), 404


# DELETE employee
@app.route("/api/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    employees = load_employees()
    filtered = [emp for emp in employees if emp["id"] != emp_id]

    if len(filtered) == len(employees):
        return jsonify({"error": "Employee not found"}), 404

    save_employees(filtered)
    return "", 204  # No content


if __name__ == "__main__":
    # host="0.0.0.0" optional if you want to access from other devices
    app.run(debug=True)
