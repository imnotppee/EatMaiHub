from flask import jsonify

def register_sunbae_routes(app, get_conn):
    @app.route("/api/sunbae", methods=["GET"])
    def get_sunbae():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.shop_name, s.review, s.banner, s.menu_name, s.menu_image
            FROM sunbae s
            ORDER BY s.id ASC;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # ✅ ถ้าไม่มีข้อมูลเลย
        if not rows:
            return jsonify({"error": "no data"}), 404

        # ✅ ดึงข้อมูลแถวแรกเป็นชื่อร้าน / รีวิว / แบนเนอร์
        first = rows[0]
        shop_name, review, banner, _, _ = first

        # ✅ สร้างโครงสร้าง JSON
        data = {
            "name": shop_name,
            "review": review,
            "banner": [f"http://127.0.0.1:5001/images/{banner}"],
            "menus": [
                {
                    "name": menu_name,
                    "image": f"http://127.0.0.1:5001/images/{menu_image}"
                }
                for _, _, _, menu_name, menu_image in rows
            ]
        }

        return jsonify(data)
