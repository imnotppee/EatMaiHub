# horoscope_route.py
from flask import Blueprint, jsonify
import psycopg2

# ✅ สร้าง Blueprint สำหรับ API กินตามดวง
horoscope_bp = Blueprint("horoscope", __name__)

# ✅ เชื่อมต่อฐานข้อมูล PostgreSQL
def get_conn():
    return psycopg2.connect(
        host="10.117.10.236",   # ✅ IP ฐานข้อมูลจริง
        port="5432",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"
    )

# ✅ สร้าง route สำหรับ API
@horoscope_bp.route("/api/horoscope", methods=["GET"])
def get_horoscope():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT day_name, category, title, subtitle, image
        FROM horoscope_foods
        ORDER BY day_name, id;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    horoscope_data = {}
    for r in rows:
        day = r[0]
        if day not in horoscope_data:
            horoscope_data[day] = []
        horoscope_data[day].append({
            "category": r[1],
            "title": r[2],
            "subtitle": r[3],
            "image": r[4]
        })
    return jsonify(horoscope_data)
