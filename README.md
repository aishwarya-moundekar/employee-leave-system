<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Backend-Flask%20%7C%20Python-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Database-MySQL-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20JavaScript-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Deployed%20On-Render%20%2B%20GitHub%20Pages-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

# Employee Leave Tracking System

A complete **full-stack Leave Tracking System** that enables organizations to efficiently manage employee leave requests.

The backend is built using **Flask (Python)** and **MySQL**, while the frontend is a UI built using **HTML, CSS, and JavaScript**.

This project highlights:

* RESTful API development
* Secure & scalable SQL schema design
* Business rule enforcement (validations, leave calculations, approvals)
* Fully integrated frontend ↔ backend workflow
* Deployment on **GitHub Pages (UI)** and **Render (API)**

This project demonstrates skills in:

*✅ API development
*✅ SQL schema design
*✅ Business logic implementation
*✅ Full frontend–backend integration
*✅ Deployment on GitHub Pages & Render

---

## 🌐 Live Demo

| Component                   | Link                                                                                                                            |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend (GitHub Pages)** | 🔗 [https://aishwarya-moundekar.github.io/employee-leave-system/](https://aishwarya-moundekar.github.io/employee-leave-system/) |
| **Backend API (Render)**    | 🔗 [https://employee-leave-system-x9i9.onrender.com](https://employee-leave-system-x9i9.onrender.com)                           |

---

## ✨ Features

### 👥 Employee Management

* Add new employees
* View employee directory
* Real-time leave balance tracking

### 📝 Leave Requests

* Apply for leave
* Automatic leave day calculation
* Prevent overlapping approved leaves
* Validates date ranges

### ✔️ Leave Approvals

* Approve or Reject leave
* Auto-deduct employee leave balance
* Status lifecycle: **Pending → Approved / Rejected**

### 📅 Monthly Reports

* Fetch monthly leave history for any employee
* Useful for HR audits & payroll integration

### 🎨 Modern UI (Glassy, Animated, Neon)

* Search & filtering
* Charts showing Pending / Approved / Rejected leaves

---

## 📸 Screenshot

### **Dashboard**

![Dashboard](dashboard.png)


---

## 🛠️ Tech Stack

| Layer          | Technologies                    |
| -------------- | ------------------------------- |
| **Backend**    | Python, Flask                   |
| **Database**   | MySQL                           |
| **Frontend**   | HTML, CSS, JavaScript           |
| **Deployment** | GitHub Pages (UI), Render (API) |
| **Tools**      | Git, GitHub                     |

---

## 📁 Project Structure

```
employee-leave-system/
│
├── api.py                # Flask API routes
├── db_utils.py           # MySQL queries + business rules
├── config_example.py     # Safe example DB config
├── config.py             # Local DB config (ignored by Git)
├── index.html            # Frontend UI
├── style.css
├── script.js
├── database.sql          # MySQL schema
├── requirements.txt      # Python dependencies
├── main.py               # Optional backend runner
├── test_db.py            # DB connection test
└── README.md             # Documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Create the MySQL Database

```bash
mysql -u root -p < database.sql
```

This creates:

* `employees`
* `leave_requests`

---

### 3️⃣ Create `config.py` (This stays local)

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "yourpassword",
    "database": "employee_leave_system"
}
```

⚠️ **DO NOT upload this file to GitHub.**
Your `.gitignore` already protects it.

---

### 4️⃣ Start the Flask API

```bash
python api.py
```

Your API will run at:

```
http://127.0.0.1:5000
```

---

### 5️⃣ Open the Frontend

Just open:

```
index.html
```

The page will auto-connect to the backend API.

---

## 🔌 API Endpoints

### 👥 Employees

| Method | Endpoint     | Description    |
| ------ | ------------ | -------------- |
| POST   | `/employees` | Add employee   |
| GET    | `/employees` | List employees |

---

### 📝 Leave Requests

| Method | Endpoint | Description         |
| ------ | -------- | ------------------- |
| POST   | `/leave` | Apply leave         |
| GET    | `/leave` | List leave requests |

---

### ✔️ Approvals

| Method | Endpoint      | Description            |
| ------ | ------------- | ---------------------- |
| POST   | `/leave/<id>` | Approve / Reject leave |

Sample Body:

```json
{ "status": "Approved" }
```

---

### 📅 Monthly Summary

```
GET /summary?employee_id=1&month=12&year=2025
```

Returns all leaves for that month.

---

## 🧠 Business Logic Highlights

* ✔️ Auto-calculates leave days
* ✔️ Blocks overlapping leave ranges
* ✔️ Deducts balance only on approval
* ✔️ Clean JSON error responses
* ✔️ SQL transactions (safe commit/rollback)
* ✔️ Centralized business logic in `db_utils.py`

---

## 🎨 UI Features

* Animated floating dashboard
* Search + filtering
* Status badges
* Bar chart visualization
* Fully responsive

---

## 🎯 Learning Outcomes

* Full-stack software development
* API architecture
* SQL & transactional logic
* State management
* Frontend engineering
* Deployment workflows

---

## 🤝 Contributing

Pull requests are welcome.
For major changes, please open an issue first.

---

## 📄 License

MIT License
© 2025 Aishwarya Moundekar
