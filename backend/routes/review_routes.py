from flask import Blueprint, jsonify, request
import psycopg2, datetime

bp = Blueprint("review_routes", __name__)

def get_conn():
    return psycopg2.connect(
        host="10.117.10.236",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234",
        port=5432
    )

# ✅ ดึงรีวิวทั้งหมด
@bp.route("/api/reviews", methods=["GET"])
def get_reviews():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.review_id, r.restaurant_name, r.menu_name, r.comment, r.created_at
        FROM review r
        ORDER BY r.created_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    data = [
        {
            "id": row[0],
            "restaurant": row[1],
            "menu_name": row[2],
            "comment": row[3],
            "time": row[4].strftime("%Y-%m-%d %H:%M:%S")
        }
        for row in rows
    ]
    return jsonify(data)


# ✅ เพิ่มรีวิว
@bp.route("/api/reviews", methods=["POST"])
def add_review():
    data = request.get_json()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO review (restaurant_name, menu_name, comment, created_at)
        VALUES (%s, %s, %s, %s)
    """, (
        data["restaurant_name"],
        data["menu_name"],
        data["comment"],
        datetime.datetime.now()
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"}), 201
