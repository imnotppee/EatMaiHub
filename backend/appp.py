# backend/appp.py
from flask import Flask
from flask_cors import CORS
from favorite_api import register_favorite_routes   # ✅ เพิ่มบรรทัดนี้

app = Flask(__name__, static_folder="static", static_url_path="/images")
CORS(app)

# ✅ เรียกใช้ route ที่แยกไว้
register_favorite_routes(app)   # ✅ เรียกใช้ฟังก์ชันที่เพิ่มใหม่

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
