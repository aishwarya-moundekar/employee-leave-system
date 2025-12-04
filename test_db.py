import mysql.connector
from config import DB_CONFIG

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("Connected! MySQL version:", conn.get_server_info())
    conn.close()
except Exception as e:
    print("Connection failed:", type(e).__name__, e)
