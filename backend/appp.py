# backend/appp.py
from flask import Flask
from flask_cors import CORS
import psycopg2

# ✅ import component ทั้งหมด
from backend.component.horoscope_component import create_horoscope_blueprint
from backend.component.review2_component import register_review_routes
from backend.component.favorite2_component import register_favorite_routes
from backend.component.urban_street_component import register_urban_street_routes
from backend.component.eat_by_color import register_eat_by_color_routes
from backend.component.highlight_component import register_highlight_routes
from backend.component.sunbae_component import register_sunbae_routes

# 🌍 CONFIG ส่วนกลาง
DB_CONFIG = {
    "host": "10.117.9.238",      # ✅ IP ของ PostgreSQL
    "database": "Eat_Mai_Hub",
    "user": "postgres",
    "password": "1234",
    "port": 5432,
}

# ✅ สร้าง Flask App
app = Flask(__name__, static_folder="static", static_url_path="/images")
CORS(app)

# ✅ ฟังก์ชันสร้างการเชื่อมต่อฐานข้อมูล
def get_conn():
    return psycopg2.connect(**DB_CONFIG)

# ✅ Register routes ทั้งหมด
register_review_routes(app, get_conn)
register_favorite_routes(app, get_conn)
register_urban_street_routes(app, get_conn)
register_eat_by_color_routes(app, get_conn)
register_highlight_routes(app, get_conn)
register_sunbae_routes(app, get_conn)

# ✅ Horoscope blueprint (เชื่อมกับระบบดูดวง)
horoscope_bp = create_horoscope_blueprint(DB_CONFIG)
app.register_blueprint(horoscope_bp)

# ✅ จุดเริ่มรัน Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
