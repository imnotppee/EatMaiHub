import json
import psycopg2
import os

# 📁 path ไปยังไฟล์ JSON
json_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "data", "random_food.json")

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
    # ใช้ .get() เพื่อป้องกัน KeyError หากไม่มี 'type'
    cur.execute("""
        INSERT INTO foods (name, image, type)
        VALUES (%s, %s, %s)
        ON CONFLICT (name) DO NOTHING;
    """, (food["name"], food["image"], food.get("type", None)))

# ✅ ปิดการเชื่อมต่ออย่างถูกลำดับ
conn.commit()
cur.close()
conn.close()

print("✅ นำเข้าข้อมูลเรียบร้อยแล้ว!")
