from flask import Blueprint, jsonify, request
import psycopg2, datetime

bp = Blueprint("favorite_routes", __name__)

def get_conn():
    return psycopg2.connect(
        host="10.117.10.236",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234",
        port=5432
    )

# ✅ ดึงรายการโปรดทั้งหมด
@bp.route("/api/favorites", methods=["GET"])
def get_favorites():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.fav_id, r.name, r.image_url, f.created_at
        FROM favorites f
        JOIN restaurants r ON f.restaurant_id = r.id
        ORDER BY f.created_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    data = [
        {
            "id": r[0],
            "title": r[1],
            "image": f"http://127.0.0.1:5001/images/{r[2]}",
            "time": r[3].strftime("%Y-%m-%d %H:%M:%S")
        }
        for r in rows
    ]
    return jsonify(data)


# ✅ เพิ่มรายการโปรด
@bp.route("/api/favorites", methods=["POST"])
def add_favorite():
    data = request.get_json()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO favorites (user_id, restaurant_id, created_at)
        VALUES (%s, %s, %s)
    """, (
        data.get("user_id", 1),
        data["restaurant_id"],
        datetime.datetime.now()
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "added"}), 201


# ✅ ลบรายการโปรด
@bp.route("/api/favorites/<int:restaurant_id>", methods=["DELETE"])
def delete_favorite(restaurant_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM favorites WHERE restaurant_id = %s", (restaurant_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "removed"}), 200
