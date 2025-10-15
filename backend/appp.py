# backend/appp.py
from flask import Flask
from flask_cors import CORS
import psycopg2

from favorite_api import register_favorite_routes

app = Flask(__name__, static_folder="static", static_url_path="/images")
CORS(app)

# -------------------- 🔌 ฟังก์ชันเชื่อมต่อฐานข้อมูล --------------------
def get_conn():
    return psycopg2.connect(
        host="10.117.9.238",       # IP Server ของ PostgreSQL
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"
    )

# ✅ ส่งต่อฟังก์ชัน get_conn ไปให้ favorite_api ใช้
register_favorite_routes(app, get_conn)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
