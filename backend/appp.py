from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# ✅ เชื่อมต่อฐานข้อมูล PostgreSQL
def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"
    )

# -------------------- 📦 API: ดึงข้อมูลร้านอาหาร --------------------
@app.route("/api/foods", methods=["GET"])
def get_foods():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, image_url, location, open_hours FROM restaurants;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    foods = [
        {"id": r[0], "name": r[1], "image": r[2], "location": r[3], "open_hours": r[4]}
        for r in rows
    ]
    return jsonify(foods)

# -------------------- 🌟 API: ดึงข้อมูล highlight --------------------
@app.route("/api/highlights", methods=["GET"])
def get_highlights():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, image_url FROM highlights;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    highlights = [
        {"id": r[0], "name": r[1], "desc": r[2], "image": r[3]}
        for r in rows
    ]
    return jsonify(highlights)

# -------------------- ❤️ API: ดึงข้อมูล favorites --------------------
@app.route("/api/favorites/<int:user_id>", methods=["GET"])
def get_favorites(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.id, r.name, r.image_url, r.location, r.open_hours
        FROM favorites f
        JOIN restaurants r ON f.restaurant_id = r.id
        WHERE f.user_id = %s
        ORDER BY f.created_at DESC;
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    favorites = [
        {
            "id": r[0],
            "title": r[1],
            "image": r[2],
            "location": r[3],
            "open_hours": r[4]
        }
        for r in rows
    ]
    return jsonify(favorites)

# ✅ เพิ่ม / ลบ favorite
@app.route("/api/favorites/toggle", methods=["POST"])
def toggle_favorite():
    data = request.get_json()
    user_id = data["user_id"]
    restaurant_id = data["restaurant_id"]

    conn = get_conn()
    cur = conn.cursor()

    # ตรวจสอบว่ามีอยู่แล้วไหม
    cur.execute("SELECT * FROM favorites WHERE user_id=%s AND restaurant_id=%s", (user_id, restaurant_id))
    exists = cur.fetchone()

    if exists:
        cur.execute("DELETE FROM favorites WHERE user_id=%s AND restaurant_id=%s", (user_id, restaurant_id))
        conn.commit()
        status = "removed"
    else:
        cur.execute(
            "INSERT INTO favorites (user_id, restaurant_id, created_at) VALUES (%s, %s, NOW())",
            (user_id, restaurant_id),
        )
        conn.commit()
        status = "added"

    cur.close()
    conn.close()
    return jsonify({"status": status})

# -------------------- 🚀 Run server --------------------
if __name__ == "__main__":
    app.run(port=5001, debug=True)
