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

# -------------------- 🍱 API: ดึงข้อมูล foods --------------------
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

# -------------------- 🌟 API: ดึงข้อมูล highlights --------------------
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

# -------------------- 🚀 Run server --------------------
if __name__ == "__main__":
    app.run(port=5001, debug=True)