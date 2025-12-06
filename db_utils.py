# db_utils.py
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Employee functions
def add_employee_db(name, total_leave_balance=20):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO employees (name, total_leave_balance) VALUES (%s, %s)", (name, total_leave_balance))
    conn.commit()
    emp_id = cur.lastrowid
    cur.close()
    conn.close()
    return {"employee_id": emp_id, "name": name, "total_leave_balance": total_leave_balance}

def list_employees_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT employee_id, name, total_leave_balance FROM employees")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = [{"employee_id": r[0], "name": r[1], "total_leave_balance": r[2]} for r in rows]
    return result

# Leave functions
def apply_leave_db(employee_id, leave_type, start_date, end_date):
    # validate dates and calculate days
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    if end < start:
        raise ValueError("end_date cannot be before start_date")
    days = (end - start).days + 1

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT total_leave_balance FROM employees WHERE employee_id=%s", (employee_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        raise LookupError("employee_not_found")
    balance = row[0]
    if days > balance:
        cur.close(); conn.close()
        raise ValueError("insufficient_balance")

    # check overlap with approved leaves
    cur.execute("""
        SELECT COUNT(*) FROM leave_requests
        WHERE employee_id=%s AND status='Approved'
          AND NOT (end_date < %s OR start_date > %s)
    """, (employee_id, start_date, end_date))
    if cur.fetchone()[0] > 0:
        cur.close(); conn.close()
        raise ValueError("overlap_with_existing_approved_leave")

    cur.execute("""
        INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, days)
        VALUES (%s, %s, %s, %s, %s)
    """, (employee_id, leave_type, start_date, end_date, days))
    conn.commit()
    req_id = cur.lastrowid
    cur.close(); conn.close()
    return {"request_id": req_id, "employee_id": employee_id, "days": days, "status": "Pending"}

def list_requests_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT request_id, employee_id, leave_type, start_date, end_date, days, status FROM leave_requests")
    rows = cur.fetchall()
    cur.close(); conn.close()
    result = []
    for r in rows:
        result.append({
            "request_id": r[0],
            "employee_id": r[1],
            "leave_type": r[2],
            "start_date": r[3].isoformat(),
            "end_date": r[4].isoformat(),
            "days": r[5],
            "status": r[6]
        })
    return result

def update_leave_status_db(request_id, status):
    if status not in ("Approved", "Rejected"):
        raise ValueError("invalid_status")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT employee_id, days, status FROM leave_requests WHERE request_id=%s", (request_id,))
    row = cur.fetchone()
    if not row:
        cur.close(); conn.close()
        raise LookupError("request_not_found")
    emp_id, days, cur_status = row
    if cur_status == status:
        cur.close(); conn.close()
        return {"request_id": request_id, "status": cur_status, "message": "no_change"}

    cur.execute("UPDATE leave_requests SET status=%s WHERE request_id=%s", (status, request_id))
    if status == "Approved":
        cur.execute("UPDATE employees SET total_leave_balance = total_leave_balance - %s WHERE employee_id=%s", (days, emp_id))
    conn.commit()
    cur.close(); conn.close()
    return {"request_id": request_id, "new_status": status}

def monthly_summary_db(employee_id, month, year=None):
    if not year:
        year = datetime.now().year
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT request_id, leave_type, days, status, applied_on
        FROM leave_requests
        WHERE employee_id=%s AND MONTH(applied_on)=%s AND YEAR(applied_on)=%s
    """, (employee_id, month, year))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return [
        {"request_id": r[0], "leave_type": r[1], "days": r[2], "status": r[3], "applied_on": r[4].isoformat()}
        for r in rows
    ]

