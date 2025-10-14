# appp.py
from flask import Flask
from flask_cors import CORS
from horoscope_route import horoscope_bp  # ✅ import route ที่แยกไว้

app = Flask(__name__)
CORS(app)

# ✅ ลงทะเบียน Blueprint
app.register_blueprint(horoscope_bp)

# ✅ จุดเริ่มรัน Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
