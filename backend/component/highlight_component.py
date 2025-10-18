from fastapi import APIRouter
from fastapi.responses import JSONResponse

def register_highlight_routes(app, get_conn):
    @app.get("/api/highlights")
    def get_highlights():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, image, description
            FROM highlights
            ORDER BY id ASC;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        data = [
            {
                "id": r[0],
                "name": r[1],
                "image": f"http://127.0.0.1:8000/images/{r[2]}",
                "desc": r[3],
            }
            for r in rows
        ]
        return JSONResponse(content=data)
