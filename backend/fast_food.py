import json
import psycopg2
import os

# 📁 กำหนด path ไปยังไฟล์ JSON
json_path = os.path.join(os.path.dirname(__file__), "frontend", "data", "random_food.json")

# 🔌 เชื่อมต่อ PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="Eat_Mai_Hub",
    user="postgres",
    password="1234"
)
cur = conn.cursor()

# 📥 อ่านข้อมูลจาก JSON
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 🧾 วนลูป insert ทีละรายการ
for food in data["foods"]:
    cur.execute(
        "INSERT INTO foods (name, image, type) VALUES (%s, %s, %s)",
        (food["name"], food["image"], food["type"])
    )

conn.commit()
cur.close()
conn.close()
print("✅ นำเข้าข้อมูลเรียบร้อยแล้ว!")
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"
    )

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
