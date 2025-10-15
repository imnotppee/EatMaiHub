# appp.py
from flask import Flask
from flask_cors import CORS
from backend.component.horoscope_component import create_horoscope_blueprint  # ✅ import ฟังก์ชันสร้าง blueprint

app = Flask(__name__)
CORS(app)

# ✅ กำหนดค่าฐานข้อมูล (localhost)
DB_CONFIG = {
    "host": "10.117.9.238",    # หรือเปลี่ยนเป็น "10.117.9.238" สำหรับเครื่องจริง
    "port": "5432",
    "database": "Eat_Mai_Hub",
    "user": "postgres",
    "password": "1234"
}

# ✅ สร้าง Blueprint พร้อมส่ง config เข้าไป
horoscope_bp = create_horoscope_blueprint(DB_CONFIG)
app.register_blueprint(horoscope_bp)

# ✅ จุดเริ่มรัน Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
