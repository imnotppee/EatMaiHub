from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Review, Restaurant, User
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/review", tags=["Review"])

# -------------------- 🧩 Database Dependency --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- 🧱 Schema --------------------
class ReviewResponse(BaseModel):
    review_id: int
    restaurant_name: Optional[str]
    restaurant_image: Optional[str]   # ✅ รูปภาพร้าน
    username: Optional[str]
    rating: int
    comment: Optional[str]

    class Config:
        orm_mode = True


# -------------------- 💬 ดึงข้อมูลรีวิวทั้งหมด --------------------
@router.get("/", response_model=List[ReviewResponse])
def get_all_reviews(db: Session = Depends(get_db)):
    """
    ดึงข้อมูลรีวิวทั้งหมด พร้อมชื่อร้าน รูปภาพร้าน และชื่อผู้ใช้
    """
    try:
        BASE_URL = "http://127.0.0.1:8000/static/images/"  # ✅ base path สำหรับรูป

        reviews = (
            db.query(
                Review.review_id,
                Restaurant.__table__.c.name.label("restaurant_name"),
                Restaurant.__table__.c.image_url.label("restaurant_image"),
                User.username,
                Review.rating,
                Review.comment
            )
            .join(User, User.user_id == Review.user_id)
            .join(Restaurant, Restaurant.__table__.c.id == Review.restaurant_id)
            .order_by(Review.review_id.desc())
            .all()
        )

        # ✅ เติม URL เต็มให้รูปภาพ (ถ้ายังไม่เป็น http)
        result = []
        for r in reviews:
            img = r.restaurant_image
            if img and not img.startswith("http"):
                img = BASE_URL + img
            result.append(
                ReviewResponse(
                    review_id=r.review_id,
                    restaurant_name=r.restaurant_name,
                    restaurant_image=img,
                    username=r.username,
                    rating=r.rating,
                    comment=r.comment
                )
            )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
