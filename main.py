# main.py
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print("Error connecting to DB:", e)
        raise

def init_db():
    # just to test connection - DB created via database.sql
    conn = get_connection()
    conn.close()

def add_employee(name, total_leave_balance=20):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO employees (name, total_leave_balance) VALUES (%s, %s)"
    cursor.execute(query, (name, total_leave_balance))
    conn.commit()
    emp_id = cursor.lastrowid
    cursor.close()
    conn.close()
    print(f"Employee Added! employee_id={emp_id}")
    return emp_id

def calculate_days(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    if end < start:
        raise ValueError("end date cannot be earlier than start date")
    return (end - start).days + 1

def apply_leave(employee_id, leave_type, start_date, end_date):
    days = calculate_days(start_date, end_date)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT total_leave_balance FROM employees WHERE employee_id=%s", (employee_id,))
    row = cursor.fetchone()
    if not row:
        print("Employee not found.")
        cursor.close()
        conn.close()
        return
    balance = row[0]
    if days > balance:
        print("Error: Not enough leave balance.")
        cursor.close()
        conn.close()
        return

    # Optional: check overlap with approved leaves
    cursor.execute("""
        SELECT COUNT(*) FROM leave_requests
        WHERE employee_id=%s AND status='Approved'
        AND NOT (end_date < %s OR start_date > %s)
    """, (employee_id, start_date, end_date))
    overlap = cursor.fetchone()[0]
    if overlap > 0:
        print("Error: Overlaps with existing approved leave.")
        cursor.close()
        conn.close()
        return

    query = """
        INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, days)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (employee_id, leave_type, start_date, end_date, days))
    conn.commit()
    req_id = cursor.lastrowid
    cursor.close()
    conn.close()
    print(f"Leave Applied Successfully! request_id={req_id}, status=Pending")

def update_leave_status(request_id, status):
    if status not in ("Approved", "Rejected"):
        print("Status must be Approved or Rejected")
        return
    conn = get_connection()
    cursor = conn.cursor()
    # get current status and data
    cursor.execute("SELECT employee_id, days, status FROM leave_requests WHERE request_id=%s", (request_id,))
    row = cursor.fetchone()
    if not row:
        print("Leave request not found.")
        cursor.close()
        conn.close()
        return
    emp_id, days, cur_status = row
    if cur_status == status:
        print("No change in status.")
        cursor.close()
        conn.close()
        return

    cursor.execute("UPDATE leave_requests SET status=%s WHERE request_id=%s", (status, request_id))
    # If approved, deduct leave balance
    if status == "Approved":
        cursor.execute("UPDATE employees SET total_leave_balance = total_leave_balance - %s WHERE employee_id=%s",
                       (days, emp_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Leave {status} Successfully for request_id={request_id}")

def monthly_summary(employee_id, month, year=None):
    conn = get_connection()
    cursor = conn.cursor()
    if not year:
        year = datetime.now().year
    query = """
        SELECT request_id, leave_type, days, status, applied_on 
        FROM leave_requests 
        WHERE employee_id=%s AND MONTH(applied_on)=%s AND YEAR(applied_on)=%s
    """
    cursor.execute(query, (employee_id, month, year))
    result = cursor.fetchall()
    print("\nMonthly Leave Summary:")
    for row in result:
        print(row)
    cursor.close()
    conn.close()

def list_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT employee_id, name, total_leave_balance FROM employees")
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()

def list_leave_requests():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT request_id, employee_id, leave_type, start_date, end_date, days, status FROM leave_requests")
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()

# Simple interactive CLI for quick manual testing
def cli():
    print("Employee Leave System CLI")
    while True:
        print("\nOptions: add_emp | list_emp | apply | list_req | update | summary | exit")
        cmd = input("Enter option: ").strip().lower()
        try:
            if cmd == "add_emp":
                name = input("Name: ")
                bal = input("Total leave balance (default 20): ").strip()
                bal = int(bal) if bal else 20
                add_employee(name, bal)
            elif cmd == "list_emp":
                list_employees()
            elif cmd == "apply":
                emp = int(input("employee_id: "))
                ltype = input("leave_type: ")
                s = input("start_date (YYYY-MM-DD): ")
                e = input("end_date (YYYY-MM-DD): ")
                apply_leave(emp, ltype, s, e)
            elif cmd == "list_req":
                list_leave_requests()
            elif cmd == "update":
                req = int(input("request_id: "))
                st = input("status (Approved/Rejected): ")
                update_leave_status(req, st)
            elif cmd == "summary":
                emp = int(input("employee_id: "))
                m = int(input("month (1-12): "))
                y = input("year (press enter for current): ").strip()
                y = int(y) if y else None
                monthly_summary(emp, m, y)
            elif cmd == "exit":
                break
            else:
                print("Unknown command.")
        except Exception as ex:
            print("Error:", ex)

if __name__ == "__main__":
    cli()
