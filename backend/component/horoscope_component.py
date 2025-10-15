# backend/component/horoscope_component.py
from fastapi import APIRouter, Request
from sqlalchemy import text
from database import engine

router = APIRouter(prefix="/api", tags=["Horoscope"])

@router.get("/horoscope")
def get_horoscope(request: Request):
    base_url = str(request.base_url).rstrip("/")  # http://127.0.0.1:8000
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT day_name, category, title, subtitle, image
            FROM horoscope_foods
            ORDER BY day_name, id;
        """))
        rows = result.fetchall()

    horoscope_data = {}
    for r in rows:
        day = r[0]
        if day not in horoscope_data:
            horoscope_data[day] = []
        horoscope_data[day].append({
            "category": r[1],
            "title": r[2],
            "subtitle": r[3],
            # ✅ สร้าง URL ของรูป
            "image": f"{base_url}/images/{r[4]}"
        })

    return horoscope_data
