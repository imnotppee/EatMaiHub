from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db  # สมมติคุณมีไฟล์ database.py
from models import Restaurant, Category  # สมมติคุณมีไฟล์ models.py

# ✅ สร้าง router ก่อนใช้งาน
router = APIRouter(prefix="/api", tags=["categories"])

@router.get("/restaurants")
def get_restaurants(request: Request, category: str | None = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Restaurant)

        if category:
            query = query.join(Category).filter(Category.category_name == category)

        restaurants = query.all()
        result = []

        for r in restaurants:
            category_name = r.category.category_name if getattr(r, "category", None) else None
            if not category_name:
                category_name = {
                    1: "fast_foods",
                    2: "japan_foods",
                    3: "thai_foods"
                }.get(r.category_id)

            # ใช้ image_url จาก DB หรือ fallback
            if r.image_url:
                image_url = r.image_url
            else:
                safe_name = r.name.replace(" ", "_")
                image_url = f"/static/images/{safe_name}.jpg"

            full_image_url = str(request.base_url).rstrip("/") + image_url

            restaurant_item = {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "image_url": full_image_url,
                "location": r.location,
                "is_featured": r.is_featured,
                "open_hours": r.open_hours,
                "category_name": category_name
            }
            result.append(restaurant_item)

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
