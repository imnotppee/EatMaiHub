from fastapi.responses import JSONResponse

def register_sunbae_routes(app, get_conn):
    @app.get("/api/sunbae")
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

        if not rows:
            return JSONResponse(content={"error": "no data"}, status_code=404)

        first = rows[0]
        shop_name, review, banner, _, _ = first

        data = {
            "name": shop_name,
            "review": review,
            "banner": [f"http://127.0.0.1:8000/images/{banner}"],
            "menus": [
                {
                    "name": menu_name,
                    "image": f"http://127.0.0.1:8000/images/{menu_image}"
                }
                for _, _, _, menu_name, menu_image in rows
            ]
        }

        return JSONResponse(content=data)
