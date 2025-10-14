# backend/review_api.py
from flask import Blueprint, jsonify, request
import psycopg2

review_api = Blueprint("review_api", __name__)

def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"
    )

# ดึงรีวิวทั้งหมด
@review_api.route("/api/review", methods=["GET"])
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


# เพิ่มรีวิวใหม่
@review_api.route("/api/review", methods=["POST"])
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
