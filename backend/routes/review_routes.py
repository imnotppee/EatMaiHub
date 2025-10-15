from flask import Blueprint, jsonify, request
import datetime

def register_review_routes(app, get_conn):
    bp = Blueprint("review_routes", __name__)

    # ✅ เพิ่มรีวิวใหม่
    @bp.route("/api/reviews", methods=["POST"])
    def add_review():
        data = request.get_json()
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO review (
                    restaurant_name,
                    menu_name,
                    rating,
                    review_text,
                    user_id,
                    restaurant_table
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                data.get("restaurant_table"),  # ← ใช้ชื่อร้านเก็บใน restaurant_name ด้วย
                data.get("menu_name"),         # ← ชื่อเมนู
                data.get("stars"),             # ← คะแนน
                data.get("comment"),           # ← รีวิวข้อความ
                data.get("user_id"),           # ← ID ผู้ใช้
                data.get("restaurant_table")   # ← ชื่อร้านเก็บใน restaurant_table อีกที่
            ))
            conn.commit()
            return jsonify({"status": "review_added"}), 201

        except Exception as e:
            conn.rollback()
            print("❌ ERROR:", e)
            return jsonify({"error": str(e)}), 500

        finally:
            cur.close()
            conn.close()

    # ✅ ดึงรีวิวทั้งหมด
    @bp.route("/api/reviews", methods=["GET"])
    def get_reviews():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT restaurant_name, menu_name, rating, review_text, user_id, restaurant_table
            FROM review
            ORDER BY rating DESC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        data = [
            {
                "restaurant_name": r[0],
                "menu_name": r[1],
                "stars": r[2],
                "comment": r[3],
                "user_id": r[4],
                "restaurant_table": r[5]
            }
            for r in rows
        ]
        return jsonify(data)

    app.register_blueprint(bp)
