from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import bcrypt

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

# ✅ Route ทดสอบ API
@app.route("/")
def home():
    return jsonify({"message": "EatMaiHub API is running on port 5001!"})

# ✅ สมัครสมาชิก (Register)
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password").encode('utf-8')
    email = data.get("email")

    # เข้ารหัส password
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password, email, created_at)
            VALUES (%s, %s, %s, NOW())
            """,
            (username, hashed.decode('utf-8'), email)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201

    except psycopg2.Error as e:
        conn.rollback()
        print("Database error:", e)
        return jsonify({"error": str(e)}), 400


# ✅ ล็อกอิน (Login)
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password").encode('utf-8')

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password, user[0].encode('utf-8')):
        return jsonify({"message": "Login success!"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)
# ✅ สร้างแอปพลิเคชัน Flask และเปิดใช้งาน CORS