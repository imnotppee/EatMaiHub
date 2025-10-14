# backend/urban_street.py
from flask import jsonify
import psycopg2

def get_conn():
    return psycopg2.connect(
        host="10.117.10.236",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234",
        port=5432
    )

def register_urban_street_routes(app):
    @app.route("/api/urban-street", methods=["GET"])
    def get_urban_street():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT u.shop_name, u.review, u.banner, u.menu_name, u.menu_image
            FROM urban_street u
            ORDER BY u.id ASC;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # ✅ สร้าง JSON
        if not rows:
            return jsonify({"error": "no data"}), 404

        first = rows[0]
        shop_name, review, banner, _, _ = first

        data = {
            "name": shop_name,
            "review": review,
            "banner": [f"http://127.0.0.1:5001/images/{banner}"],
            "menus": [
                {
                    "name": menu_name,
                    "image": f"http://127.0.0.1:5001/images/{menu_image}"
                }
                for _, _, _, menu_name, menu_image in rows
            ]
        }
        return jsonify(data)
