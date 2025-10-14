from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

# -------------------- ⚙️ ตั้งค่าแอป --------------------
app = Flask(__name__)
CORS(app)

# -------------------- 🧩 ฟังก์ชันเชื่อมต่อฐานข้อมูล --------------------
def get_conn():
    return psycopg2.connect(
        host="10.117.10.236",   # ✅ ใช้ IP เดียวกับใน pgAdmin
        port=5432,
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"         # ✅ ใส่รหัสเดียวกับใน pgAdmin
    )


# -------------------- 🏠 หน้า Home --------------------
@app.route("/")
def home():
    return jsonify({"message": "✅ EatMaiHub Backend is running!"})


# -------------------- 🍽️ API: ดึงข้อมูลอาหาร --------------------
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


# -------------------- 🌟 API: ดึงข้อมูลร้านอาหารตามหมวดหมู่ --------------------
@app.route("/api/restaurants", methods=["GET"])
def get_restaurants():
    category_name = request.args.get("category")
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT r.name, r.description, r.image_url, r.location, r.is_featured,
               r.open_hours, c.category_name
        FROM restaurants r
        JOIN categories c ON r.category_id = c.category_id
        WHERE c.category_name = %s;
    """, (category_name,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = [
        {
            "name": r[0],
            "description": r[1],
            "image": r[2],
            "location": r[3],
            "is_featured": r[4],
            "open_hours": r[5],
            "category": r[6],
        } for r in rows
    ]
    return jsonify(result)


# -------------------- 💬 API: ดึงข้อมูลรีวิวทั้งหมด --------------------
@app.route("/api/review", methods=["GET"])
def get_review():
    conn = get_conn()
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


# -------------------- 🆕 API: เพิ่มรีวิวใหม่ --------------------
@app.route("/api/review", methods=["POST"])
def add_review():
    data = request.get_json()
    conn = get_conn()
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


# -------------------- 🚀 รันเซิร์ฟเวอร์ --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
