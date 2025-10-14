# backend/eat_by_color.py
from flask import jsonify
import psycopg2

# -------------------- 🧩 ฟังก์ชันเชื่อมต่อฐานข้อมูล --------------------
def get_conn():
    return psycopg2.connect(
        host="10.117.10.236",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234",
        port=5432
    )

# -------------------- 🌈 ฟังก์ชันลงทะเบียน route --------------------
def register_eat_by_color_routes(app):
    @app.route("/api/color-menus", methods=["GET"])
    def get_color_menus():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.color_key, cm.food_name, cm.image_url
            FROM colors c
            JOIN colormenus cm ON cm.color_id = c.id
            ORDER BY c.id;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        data = {}
        for color_key, food_name, image_url in rows:
            data.setdefault(color_key, []).append({
                "name": food_name,
                "image": f"http://127.0.0.1:5001/images/{image_url}"
            })

        return jsonify(data)
