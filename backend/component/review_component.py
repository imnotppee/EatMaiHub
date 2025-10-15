# backend/review_api.py
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
    username: Optional[str]
    rating: int
    comment: Optional[str]

    class Config:
        orm_mode = True


# -------------------- 💬 ดึงข้อมูลรีวิวทั้งหมด --------------------
@router.get("/", response_model=List[ReviewResponse])
def get_all_reviews(db: Session = Depends(get_db)):
    """
    ดึงข้อมูลรีวิวทั้งหมด พร้อมชื่อร้านและชื่อผู้ใช้
    """
    try:
        # ✅ ใช้ชื่อ column จริงในฐานข้อมูล (id)
        reviews = (
            db.query(
                Review.review_id,
                Restaurant.__table__.c.name.label("restaurant_name"),
                User.username,
                Review.rating,
                Review.comment
            )
            .join(User, User.user_id == Review.user_id)
            .join(Restaurant, Restaurant.__table__.c.id == Review.restaurant_id)
            .order_by(Review.review_id.desc())
            .all()
        )

        # ✅ แปลงเป็น list ของ dict
        return [
            ReviewResponse(
                review_id=r.review_id,
                restaurant_name=r.restaurant_name,
                username=r.username,
                rating=r.rating,
                comment=r.comment
            )
            for r in reviews
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
