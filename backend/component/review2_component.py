from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import datetime

def register_review_routes(app, get_conn):
    router = APIRouter()

    # ✅ เพิ่มรีวิวใหม่
    @router.post("/api/reviews")
    async def add_review(request: Request):
        data = await request.json()
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO review (
                    restaurant_name,
                    menu_name,
                    rating,
                    review_text,
                    user_id,
                    restaurant_table
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                data.get("restaurant_table"),
                data.get("menu_name"),
                data.get("stars"),
                data.get("comment"),
                data.get("user_id"),
                data.get("restaurant_table")
            ))
            conn.commit()
            return JSONResponse(content={"status": "review_added"}, status_code=201)

        except Exception as e:
            conn.rollback()
            print("❌ ERROR:", e)
            return JSONResponse(content={"error": str(e)}, status_code=500)

        finally:
            cur.close()
            conn.close()

    # ✅ ดึงรีวิวทั้งหมด
    @router.get("/api/reviews")
    def get_reviews():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT restaurant_name, menu_name, rating, review_text, user_id, restaurant_table
            FROM review
            ORDER BY rating DESC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        data = [
            {
                "restaurant_name": r[0],
                "menu_name": r[1],
                "stars": r[2],
                "comment": r[3],
                "user_id": r[4],
                "restaurant_table": r[5]
            }
            for r in rows
        ]
        return JSONResponse(content=data)

    app.include_router(router)
