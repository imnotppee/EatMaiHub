# backend/review_api.py
from flask import Blueprint, jsonify, request, current_app

# ✅ สร้าง Blueprint
review_api = Blueprint("review_api", __name__)

# -------------------- 💬 ดึงข้อมูลรีวิวทั้งหมด --------------------
@review_api.route("/api/review", methods=["GET"])
def get_review():
    conn_func = current_app.config["GET_CONN"]  # ดึงฟังก์ชัน get_conn จาก app.py
    conn = conn_func()
    cur = conn.cursor()

    cur.execute("""
        SELECT review_id, restaurant_name, menu_name, rating, review_text
        FROM review
        ORDER BY review_id DESC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    review = [
        {
            "review_id": r[0],
            "restaurant_name": r[1],
            "menu_name": r[2],
            "rating": r[3],
            "review_text": r[4]
        }
        for r in rows
    ]
    return jsonify(review)

# -------------------- ➕ เพิ่มรีวิวใหม่ --------------------
@review_api.route("/api/review", methods=["POST"])
def add_review():
    data = request.get_json()
    conn_func = current_app.config["GET_CONN"]
    conn = conn_func()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO review (restaurant_name, menu_name, rating, review_text)
        VALUES (%s, %s, %s, %s)
    """, (
        data["restaurant_name"],
        data["menu_name"],
        data["rating"],
        data["review_text"]
    ))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "✅ Review added successfully!"})
