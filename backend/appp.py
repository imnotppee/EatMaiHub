from flask import Flask
import psycopg2
from routes.review_routes import register_review_routes
from routes.favorite_routes import register_favorite_routes
from urban_street import register_urban_street_routes
from eat_by_color import register_eat_by_color_routes
from highlight import register_highlight_routes
from sunbae import register_sunbae_routes

# 🌍 CONFIG ส่วนกลาง
DB_CONFIG = {
    "host": "10.117.9.238",      # ✅ อัปเดตเป็น IP ใหม่ของ PostgreSQL
    "database": "Eat_Mai_Hub",
    "user": "postgres",
    "password": "1234",
    "port": 5432,
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

# 🚀 เริ่ม Flask
app = Flask(__name__)

register_review_routes(app, get_conn)
register_favorite_routes(app, get_conn)
register_urban_street_routes(app, get_conn)
register_eat_by_color_routes(app, get_conn)
register_highlight_routes(app, get_conn)
register_sunbae_routes(app, get_conn)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
