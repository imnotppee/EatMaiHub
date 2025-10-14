from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "host": "10.117.10.236",
    "database": "Eat_Mai_Hub",
    "user": "postgres",
    "password": "1234"
}

@app.route("/api/restaurants", methods=["GET"])
def api_restaurants():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT r.id, r.name, r.description, r.image_url, r.location, 
                       r.is_featured, r.open_hours, c.category_name
                FROM restaurants r
                LEFT JOIN categories c ON r.category_id = c.category_id
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
                    "category": r[7]
                })
        return jsonify(data)
    except Exception as e:
        print("Error fetching restaurants:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route("/api/categories", methods=["GET"])
def api_categories():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute("SELECT category_id, category_name FROM categories")
            rows = cur.fetchall()
            categories = [{"id": r[0], "name": r[1]} for r in rows]
        return jsonify(categories)
    except Exception as e:
        print("Error fetching categories:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)