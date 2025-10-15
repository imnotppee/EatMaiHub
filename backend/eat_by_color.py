from flask import jsonify

def register_eat_by_color_routes(app, get_conn):
    @app.route("/api/color-menus", methods=["GET"])
    def get_color_menus():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.color_key, cm.food_name, cm.image_url
            FROM colors c
            JOIN colormenus cm ON cm.color_id = c.id
            ORDER BY c.id;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        data = {}
        for color_key, food_name, image_url in rows:
            data.setdefault(color_key, []).append({
                "name": food_name,
                "image": f"http://127.0.0.1:5001/images/{image_url}"
            })

        return jsonify(data)
