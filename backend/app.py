from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="Eat_Mai_Hub",
        user="postgres",
        password="1234"
    )
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# ✅ เชื่อมต่อฐานข้อมูล PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="Eat_Mai_Hub",
    user="postgres",
    password="1234"
)
cursor = conn.cursor()

@app.route("/api/foods", methods=["GET"])
def get_foods():
    cursor.execute("SELECT id, name, image, type FROM foods;")
    rows = cursor.fetchall()

    foods = [
        {"id": r[0], "name": r[1], "image": r[2], "type": r[3]} for r in rows
    ]
    return jsonify(foods)

if __name__ == "__main__":
    app.run(port=5001, debug=True)


@app.route("/")
def home():
    return jsonify({"message": "EatMaiHub Backend is running ✅"})

@app.route("/api/restaurants", methods=["GET"])
def get_restaurants():
    category_name = request.args.get("category")
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT r.name, r.description, r.image_url, r.location, r.is_featured,
               r.open_hours, c.category_name
        FROM restaurants r
        JOIN categories c ON r.category_id = c.category_id
        WHERE c.category_name = %s;
    """, (category_name,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = [
        {
            "name": r[0],
            "description": r[1],
            "image": r[2],
            "location": r[3],
            "is_featured": r[4],
            "open_hours": r[5],
            "category": r[6],
        } for r in rows
    ]
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
