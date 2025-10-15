from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)


# ✅ ฟังก์ชันเชื่อมต่อฐานข้อมูล PostgreSQL
def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234",
        port=5432
    )


@app.route("/api/foods", methods=["GET"])
def api_foods():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, name, image, type FROM foods;")
        rows = cur.fetchall()
        foods = [
            {"id": r[0], "name": r[1], "image": r[2], "type": r[3]}
            for r in rows
        ]
        return jsonify(foods)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@app.route("/api/highlights", methods=["GET"])
def api_highlights():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, name, description, image_url FROM highlights;")
        rows = cur.fetchall()
        highlights = [
            {"id": r[0], "name": r[1], "desc": r[2], "image": r[3]}
            for r in rows
        ]
        return jsonify(highlights)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# -------------------- 🍽️ API: ดึงข้อมูล restaurants --------------------
@app.route("/api/restaurants", methods=["GET"])
def api_restaurants():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, description, image_url, location, is_featured, open_hours, category_id 
            FROM restaurants;
        """)
        rows = cur.fetchall()
        restaurants = [
            {
                "id": r[0],
                "name": r[1],
                "description": r[2],
                "image": r[3],
                "location": r[4],
                "is_featured": r[5],
                "open_hours": r[6],
                "category_id": r[7],
            }
            for r in rows
        ]
        return jsonify(restaurants)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# -------------------- 🎲 API: ดึงข้อมูลสุ่มอาหาร (Random) --------------------
@app.route("/api/random", methods=["GET"])
def get_random():
    conn = get_conn()
    cur = conn.cursor()

    # ✅ ใช้ชื่อ column ที่ตรงกับใน database
    cur.execute('SELECT random_id, category, menu_name, image FROM "random";')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # ✅ แปลงข้อมูลเป็น JSON
    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "category": row[1],
            "name": row[2],
            "image": row[3]
        })

    return jsonify(data)


# -------------------- 🚀 Run server --------------------
if __name__ == "__main__":
    app.run(port=5001, debug=True)