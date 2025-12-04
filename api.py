# api.py
from flask import Flask, request, jsonify
from db_utils import (add_employee_db, list_employees_db,
                      apply_leave_db, list_requests_db,
                      update_leave_status_db, monthly_summary_db)

app = Flask(__name__)

@app.route("/employees", methods=["POST"])
def add_employee():
    payload = request.json or {}
    name = payload.get("name")
    balance = payload.get("total_leave_balance", 20)
    if not name:
        return jsonify({"error": "name required"}), 400
    try:
        res = add_employee_db(name, int(balance))
        return jsonify(res), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/employees", methods=["GET"])
def list_employees():
    return jsonify(list_employees_db())

@app.route("/leave", methods=["POST"])
def apply_leave():
    payload = request.json or {}
    try:
        emp = int(payload.get("employee_id"))
        ltype = payload.get("leave_type", "Casual")
        start = payload.get("start_date")
        end = payload.get("end_date")
        if not (start and end):
            return jsonify({"error": "start_date and end_date required"}), 400
        res = apply_leave_db(emp, ltype, start, end)
        return jsonify(res), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except LookupError as le:
        return jsonify({"error": str(le)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/leave", methods=["GET"])
def list_leaves():
    return jsonify(list_requests_db())

@app.route("/leave/<int:request_id>", methods=["POST"])
def update_leave(request_id):
    payload = request.json or {}
    status = payload.get("status")
    if not status:
        return jsonify({"error": "status required"}), 400
    try:
        res = update_leave_status_db(request_id, status)
        return jsonify(res)
    except LookupError as le:
        return jsonify({"error": str(le)}), 404
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/summary", methods=["GET"])
def summary():
    emp = request.args.get("employee_id", type=int)
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    if not (emp and month):
        return jsonify({"error": "employee_id and month are required as query params"}), 400
    try:
        res = monthly_summary_db(emp, month, year)
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
