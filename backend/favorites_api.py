from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# ✅ ตั้งค่าการเชื่อมต่อ PostgreSQL
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234",  # ← ใช้รหัสที่ตั้งตอนติดตั้ง PostgreSQL
        port="5432"
    )


# ✅ ดึงรายการโปรดของผู้ใช้
@app.route('/favorites', methods=['GET'])
def get_favorites():
    user_id = request.args.get('user_id')
    print(f"\n📥 [GET] /favorites?user_id={user_id}")

    try:
        print("🔹 Connecting to database...")
        conn = get_connection()
        print("✅ Connected!")

        cur = conn.cursor(cursor_factory=RealDictCursor)
        print("🔹 Executing SQL query...")

        cur.execute("""
            SELECT 
                f.fav_id,
                r.name,
                r.image,
                r.type,
                r.rating,
                r.address,
                f.created_at
            FROM favorites f
            JOIN foods r ON f.restaurant_id = r.id
            WHERE f.user_id = %s
            ORDER BY f.created_at DESC
        """, (user_id,))

        rows = cur.fetchall()
        print(f"✅ Query completed, found {len(rows)} record(s).")

        cur.close()
        conn.close()
        print("🔒 Connection closed.\n")

        return jsonify(rows)

    except Exception as e:
        print("❌ ERROR while fetching favorites:", e)
        return jsonify({"error": str(e)})


# ✅ เพิ่มร้านในรายการโปรด (พร้อมกันซ้ำ)
@app.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    user_id = data.get('user_id')
    restaurant_id = data.get('restaurant_id')

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM favorites WHERE user_id=%s AND restaurant_id=%s", (user_id, restaurant_id))
        if cur.fetchone():
            cur.close()
            conn.close()
            print(f"⚠️ Already in favorites: user={user_id}, restaurant={restaurant_id}")
            return jsonify({"status": "exists"})

        cur.execute("""
            INSERT INTO favorites (user_id, restaurant_id, created_at)
            VALUES (%s, %s, NOW())
        """, (user_id, restaurant_id))
        conn.commit()

        cur.close()
        conn.close()

        print(f"❤️ Added favorite: user={user_id}, restaurant={restaurant_id}")
        return jsonify({"status": "added"})

    except Exception as e:
        print("❌ ERROR while adding favorite:", e)
        return jsonify({"error": str(e)})


# ✅ ลบร้านออกจากรายการโปรด
@app.route('/favorites', methods=['DELETE'])
def remove_favorite():
    data = request.get_json()
    user_id = data.get('user_id')
    restaurant_id = data.get('restaurant_id')

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM favorites WHERE user_id = %s AND restaurant_id = %s
        """, (user_id, restaurant_id))
        conn.commit()

        cur.close()
        conn.close()

        print(f"💔 Removed favorite: user={user_id}, restaurant={restaurant_id}")
        return jsonify({"status": "removed"})

    except Exception as e:
        print("❌ ERROR while removing favorite:", e)
        return jsonify({"error": str(e)})


# ✅ เริ่มต้น Flask Server
if __name__ == '__main__':
    print("🚀 Flask Server Running on http://127.0.0.1:5001")
    print("   → GET     /favorites?user_id=1")
    print("   → POST    /favorites")
    print("   → DELETE  /favorites\n")
    app.run(debug=True, port=5001)
