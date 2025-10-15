from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

#  การเชื่อมต่อฐานข้อมูล PostgreSQL
DB_CONFIG = {
    "host": "10.117.9.238",
    "database": "Eat_Mai_Hub",
    "user": "postgres",
    "password": "1234"
}

#  ฟังก์ชันดึงข้อมูลจาก restaurants 
def fetch_restaurants():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    id, 
                    name, 
                    description, 
                    image_url, 
                    location, 
                    is_featured, 
                    open_hours, 
                    category_id, 
                    category_name
                FROM restaurants
                ORDER BY id ASC;
            """)
            rows = cur.fetchall()
            data = []
            for r in rows:
                data.append({
                    "id": r[0],
                    "name": r[1],
                    "description": r[2],
                    "image_url": r[3],
                    "location": r[4],
                    "is_featured": r[5],
                    "open_hours": r[6],
                    "category_id": r[7],
                    "category_name": r[8]
                })
        return data
    finally:
        conn.close()

#  สร้าง API หลัก
@app.route("/api/restaurants", methods=["GET"])
def api_restaurants():
    try:
        data = fetch_restaurants()
        return jsonify(data)
    except Exception as e:
        print("Error fetching restaurants:", e)
        return jsonify({"error": str(e)}), 500

#  รันเซิร์ฟเวอร์ Flask
if __name__ == "__main__":
    app.run(debug=True, port=5002)