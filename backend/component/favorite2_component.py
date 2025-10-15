from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import datetime
import psycopg2

def register_favorite_routes(app, get_conn):
    router = APIRouter()

    # ✅ ดึงรายการโปรดทั้งหมด
    @router.get("/api/favorites")
    def get_favorites():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT f.fav_id, f.restaurant_id, r.name, r.image_url, f.created_at
            FROM favorites f
            JOIN restaurants r ON f.restaurant_id = r.id
            ORDER BY f.created_at DESC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        data = [
            {
                "fav_id": r[0],
                "restaurant_id": r[1],
                "title": r[2],
                "image": f"http://127.0.0.1:8000/images/{r[3]}",
                "time": r[4].strftime("%Y-%m-%d %H:%M:%S")
            }
            for r in rows
        ]
        return JSONResponse(content=data)

    # ✅ เพิ่มรายการโปรด (กันซ้ำ)
    @router.post("/api/favorites")
    async def add_favorite(request: Request):
        data = await request.json()
        user_id = data.get("user_id", 1)
        restaurant_id = data["restaurant_id"]

        conn = get_conn()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO favorites (user_id, restaurant_id, created_at)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, restaurant_id) DO NOTHING
            """, (user_id, restaurant_id, datetime.datetime.now()))
            conn.commit()

            if cur.rowcount == 0:
                message = {"status": "already_favorited"}
                status_code = 200
            else:
                message = {"status": "added"}
                status_code = 201

        except psycopg2.Error as e:
            conn.rollback()
            message = {"error": str(e)}
            status_code = 500

        finally:
            cur.close()
            conn.close()

        return JSONResponse(content=message, status_code=status_code)

    # ✅ ลบรายการโปรด (ตาม user_id + restaurant_id)
    @router.delete("/api/favorites/{restaurant_id}")
    async def delete_favorite(restaurant_id: int):
        user_id = 1  # (mock ค่า user เดียว)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM favorites 
            WHERE restaurant_id = %s AND user_id = %s
        """, (restaurant_id, user_id))
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"status": "removed"}, status_code=200)

    app.include_router(router)
