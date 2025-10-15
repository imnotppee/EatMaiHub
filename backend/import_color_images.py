import psycopg2
import json
import os

# ==============================
# CONFIG เชื่อมต่อ PostgreSQL
# ==============================
DB_CONFIG = {
    "host": "10.117.10.236",  # 🧩 ใช้ host เดียวกับ pgAdmin
    "database": "Eat_Mai_Hub",
    "user": "postgres",
    "password": "1234",       # ← ใส่รหัสจริงของคุณ
    "port": 5432
}

# ==============================
# โหลดไฟล์ JSON
# ==============================
JSON_PATH = os.path.join(os.path.dirname(__file__), "../frontend/data/color_menus.json")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    color_data = json.load(f)

# ==============================
# เชื่อมต่อฐานข้อมูล
# ==============================
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# ==============================
# สร้างตาราง (ถ้ายังไม่มี)
# ==============================
cur.execute("""
CREATE TABLE IF NOT EXISTS colors (
    id SERIAL PRIMARY KEY,
    color_key VARCHAR(20) UNIQUE NOT NULL,
    color_name_th VARCHAR(20)
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS colormenus (
    id SERIAL PRIMARY KEY,
    color_id INT REFERENCES colors(id),
    food_name VARCHAR(100),
    image_url VARCHAR(255)
);
""")
conn.commit()

# ==============================
# Insert ข้อมูล
# ==============================
color_map = {
    "red": "อาทิตย์",
    "yellow": "จันทร์",
    "pink": "อังคาร",
    "green": "พุธ",
    "orange": "พฤหัส",
    "blue": "ศุกร์",
    "purple": "เสาร์"
}

for color_key, foods in color_data.items():
    color_name_th = color_map.get(color_key, "")
    # --- เพิ่มสีถ้ายังไม่มี ---
    cur.execute("""
        INSERT INTO colors (color_key, color_name_th)
        VALUES (%s, %s)
        ON CONFLICT (color_key) DO NOTHING;
    """, (color_key, color_name_th))

    # ดึง id ของสีนั้นกลับมา
    cur.execute("SELECT id FROM colors WHERE color_key = %s;", (color_key,))
    color_id = cur.fetchone()[0]

    # --- เพิ่มเมนู ---
    for food in foods:
        name = food["name"]
        image = food["image"].replace("images/", "")  # ลบ path prefix
        cur.execute("""
            INSERT INTO colormenus (color_id, food_name, image_url)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (color_id, name, image))

conn.commit()
cur.close()
conn.close()

print("✅ นำเข้าข้อมูล color menus สำเร็จแล้ว!")
