# backend/routes/review_routes.py
from flask import Blueprint, jsonify, request
import datetime

def register_review_routes(app, get_conn):
    bp = Blueprint("review_routes", __name__)

    # ✅ ดึงรีวิวทั้งหมด
    @bp.route("/api/reviews", methods=["GET"])
    def get_reviews():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT rating, review_text, restaurant_table
            FROM review
            ORDER BY rating DESC;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        data = [
            {
                "rating": r[0],
                "review_text": r[1],
                "restaurant_table": r[2] or "-"
            }
            for r in rows
        ]
        return jsonify(data)

    # ✅ เพิ่มรีวิว
    @bp.route("/api/reviews", methods=["POST"])
    def add_review():
        data = request.get_json()
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO review (rating, review_text, restaurant_table)
            VALUES (%s, %s, %s)
        """, (
            data.get("rating"),
            data.get("review_text"),
            data.get("restaurant_table"),
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success"}), 201

    app.register_blueprint(bp)
