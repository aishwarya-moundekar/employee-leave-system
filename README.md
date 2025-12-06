# Employee Leave Tracking System

A full-stack application to manage employee leave requests with a Flask backend, MySQL database, and a modern HTML/CSS/JavaScript frontend.

This project demonstrates backend API development, SQL schema design, business rules implementation, and seamless frontend–backend integration.

---

## 📌 Features

### 👥 Employee Management

* Add new employees
* View employee directory
* Track leave balances

### 📝 Leave Requests

* Apply for leave
* Validate date ranges
* Prevent overlapping approved leave dates
* Check available leave balance before applying

### ✔️ Approvals

* Approve / Reject leave
* Automatically deduct approved leave balance
* Status lifecycle: **Pending → Approved / Rejected**

### 📅 Monthly Summary

* View an employee’s monthly leave activity
* Useful for HR audits and reporting

### 🌐 Frontend UI

* Fully responsive design
* Clean and modern look
* Connects to the Flask API using fetch()

---

## 🛠️ Tech Stack

| Layer    | Technologies          |
| -------- | --------------------- |
| Backend  | Python, Flask         |
| Database | MySQL                 |
| Frontend | HTML, CSS, JavaScript |
| Tools    | Git, GitHub           |

---

## 📁 Project Structure

```
employee-leave-system/
│
├── api.py               # Flask API routes
├── db_utils.py          # Database operations
├── main.py              # Optional CLI tool for testing
├── index.html           # Frontend UI
├── database.sql         # MySQL schema
├── requirements.txt     # Python dependencies
├── config_example.py    # Example config file
├── .gitignore           # Ignored files (including config.py)
└── README.md            # Project documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Create the MySQL Database

Run:

```bash
mysql -u root -p < database.sql
```

This creates:

* `employees` table
* `leave_requests` table

---

### 3️⃣ Create Local `config.py` (DO NOT upload to GitHub)

Inside your project folder, create:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "yourpassword",
    "database": "employee_leave_system"
}
```

> ⚠️ Do NOT commit this file.
> It is ignored by `.gitignore` to protect your credentials.

---

### 4️⃣ Start the Flask API

```bash
python api.py
```

Your API is now running at:

```
http://127.0.0.1:5000
```

---

### 5️⃣ Open the Frontend

Open `index.html` in your browser.
It will automatically connect to the backend and allow you to:

* Add employees
* Apply leave
* Approve leave
* View summaries

---

## 🔌 API Endpoints

### 👥 Employees

| Method | Endpoint     | Description    |
| ------ | ------------ | -------------- |
| POST   | `/employees` | Add employee   |
| GET    | `/employees` | List employees |

---

### 📝 Leave Requests

| Method | Endpoint | Description             |
| ------ | -------- | ----------------------- |
| POST   | `/leave` | Apply for leave         |
| GET    | `/leave` | View all leave requests |

---

### ✔️ Approvals

| Method | Endpoint              | Description            |
| ------ | --------------------- | ---------------------- |
| POST   | `/leave/<request_id>` | Approve / Reject leave |

---

### 📅 Monthly Summary

| Method | Endpoint                                    | Description     |
| ------ | ------------------------------------------- | --------------- |
| GET    | `/summary?employee_id=1&month=12&year=2025` | Monthly summary |

---

## 🧠 Business Logic Implemented

* Validate start and end dates
* Calculate leave days automatically
* Detect overlapping approved leaves
* Check employee leave balance
* Deduct balance upon approval
* Clean JSON error responses
* Safe database handling (commit, rollback, close connections)

---

## 🎯 Learning Outcomes

This project demonstrates:

* Backend API design with Flask
* SQL queries, joins, and transactions
* Clean separation of logic (`db_utils` vs `api`)
* Frontend integration using fetch API
* Secure handling of config files
* Building a complete end-to-end system

Ideal for resumes, GitHub portfolio, and interviews.

---

## 🤝 Contributing

Pull requests are welcome.
For major changes, please open an issue first.

---

## 📄 License

MIT License.

