from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# ✅ เชื่อมต่อฐานข้อมูล PostgreSQL
def get_conn():
    return psycopg2.connect(
        host="10.117.10.236",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"
    )

# -------------------- 📦 API: ดึงข้อมูลอาหาร --------------------
@app.route("/api/foods", methods=["GET"])
def get_foods():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, image, type FROM foods;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    foods = [
        {"id": r[0], "name": r[1], "image": r[2], "type": r[3]}
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

# -------------------- 💬 API: ดึงข้อมูลรีวิว --------------------
@app.route("/api/review", methods=["GET"])
def get_review():
    conn = get_conn()
    cur = conn.cursor()
    # ✅ ดึงคอลัมน์ทั้งหมดจากตาราง review
    cur.execute("""
        SELECT review_id, restaurant_name, menu_name, rating, review_text
        FROM review
        ORDER BY review_id DESC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # ✅ แปลงข้อมูลให้เป็น JSON list
    review = [
        {
            "review_id": r[0],
            "restaurant_name": r[1].strip() if r[1] else None,
            "menu_name": r[2].strip() if r[2] else None,
            "rating": r[3],
            "review_text": r[4]
        }
        for r in rows
    ]

    return jsonify(review)



if __name__ == "__main__":
    app.run(port=5001, debug=True)
