from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# ✅ เชื่อมต่อฐานข้อมูล PostgreSQL
def get_conn():
    return psycopg2.connect(
        host="10.117.15.238",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"
    )

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

# -------------------- 🚀 Run server --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
