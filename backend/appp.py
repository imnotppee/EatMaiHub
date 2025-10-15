# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from review_api import review_api   # ✅ นำเข้า Blueprint

app = Flask(__name__)
CORS(app)

# ✅ ฟังก์ชันเชื่อมต่อฐานข้อมูล (host จริงอยู่ที่นี่)
def get_conn():
    return psycopg2.connect(
        host="10.117.9.238",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"
    )

# ✅ ส่งฟังก์ชัน get_conn ให้ Blueprint ใช้ผ่าน config
app.config["GET_CONN"] = get_conn

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

# ✅ ลงทะเบียน Blueprint ของ review_api
app.register_blueprint(review_api)

# -------------------- 🚀 เริ่มรันเซิร์ฟเวอร์ --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
