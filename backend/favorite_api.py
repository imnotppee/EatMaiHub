# backend/favorite_api.py
from flask import jsonify, request
import psycopg2

# -------------------- 🔌 ฟังก์ชันเชื่อมต่อฐานข้อมูล --------------------
def get_conn():
    return psycopg2.connect(
        host="10.117.10.236",          # IP server ของ PostgreSQL
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"
    )

# -------------------- 📋 ลงทะเบียน route สำหรับ favorites --------------------
def register_favorite_routes(app):

    # 📋 ดึงรายการโปรดทั้งหมด
    @app.route("/api/favorites", methods=["GET"])
    def get_favorites():
        conn = None
        cur = None
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                SELECT f.fav_id, f.user_id, r.name, r.description, r.image_url, r.location
                FROM favorites f
                JOIN restaurants r ON f.restaurant_id = r.id
                ORDER BY f.fav_id ASC;
            """)
            rows = cur.fetchall()
            favorites = [
                {
                    "fav_id": r[0],
                    "user_id": r[1],
                    "name": r[2],
                    "description": r[3],
                    "image": r[4],
                    "location": r[5],
                }
                for r in rows
            ]
            return jsonify(favorites)
        except Exception as e:
            print("❌ ERROR get_favorites:", e)
            return jsonify({"error": str(e)}), 500
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    # ❤️ เพิ่มรายการโปรด
    @app.route("/api/favorites", methods=["POST"])
    def add_favorite():
        conn = None
        cur = None
        data = request.get_json()
        user_id = data.get("user_id")
        restaurant_id = data.get("restaurant_id")

        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO favorites (user_id, restaurant_id, created_at)
                VALUES (%s, %s, NOW())
                RETURNING fav_id;
            """, (user_id, restaurant_id))
            conn.commit()
            return jsonify({"message": "Favorite added successfully!"}), 201
        except Exception as e:
            print("❌ ERROR add_favorite:", e)
            return jsonify({"error": str(e)}), 500
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    # 💔 ลบรายการโปรด
    @app.route("/api/favorites/<int:fav_id>", methods=["DELETE"])
    def delete_favorite(fav_id):
        conn = None
        cur = None
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM favorites WHERE fav_id = %s;", (fav_id,))
            conn.commit()
            return jsonify({"message": "Favorite removed"}), 200
        except Exception as e:
            print("❌ ERROR delete_favorite:", e)
            return jsonify({"error": str(e)}), 500
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
