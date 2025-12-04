# Employee Leave Tracking System (Python + MySQL)

A backend system for managing employee leave with:
- CRUD operations
- Leave balance validation
- Approval workflows
- Monthly summary queries

## Run Steps
1. Run the SQL script:
mysql -u root -p < database.sql
2. Update `config.py` with your DB details.
3. Install requirements:
pip install -r requirements.txt
4. Run:
python main.py

## Features
- Add Employee
- Apply Leave
- Approve/Reject Leave
- Monthly Summary Reporting

## Tech Stack
Python, MySQL, SQL
