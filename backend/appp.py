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

# -------------------- 🍽️ API: ดึงข้อมูลร้านอาหารตามหมวดหมู่ --------------------
@app.route("/api/restaurants", methods=["GET"])
def get_restaurants():
    conn = get_conn()
    cur = conn.cursor()
    
    # ดึงข้อมูลทั้งหมดจากตาราง restaurants
    cur.execute("SELECT id, name, review, address, banner FROM restaurants;")
    rows = cur.fetchall()
    
    cur.close()
    conn.close()

    # แปลงข้อมูลจาก tuple → dict
    data = [
        {
            "id": r[0],
            "name": r[1],
            "review": r[2],
            "address": r[3],
            "banner": r[4]
        }
        for r in rows
    ]
    return jsonify(data)

# -------------------- 🏪 API: ดึงข้อมูลร้านอาหารตาม id --------------------
@app.route("/api/restaurants/<int:restaurant_id>", methods=["GET"])
def get_restaurant_by_id(restaurant_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, review, address, banner FROM restaurants WHERE id = %s;", (restaurant_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        restaurant = {
            "id": row[0],
            "name": row[1],
            "review": row[2],
            "address": row[3],
            "banner": row[4]
        }
        return jsonify(restaurant)
    else:
        return jsonify({"error": "Restaurant not found"}), 404


# -------------------- 🚀 Run server --------------------
if __name__ == "__main__":
    app.run(port=5001, debug=True)
