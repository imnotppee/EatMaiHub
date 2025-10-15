from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic import BaseModel
from models import Random  # ✅ ตาราง random ต้องมีใน models.py

router = APIRouter(prefix="/api", tags=["Random Food"])


# ---------- สร้าง schema สำหรับ response ----------
class RandomFoodOut(BaseModel):
    id: int
    category: str
    name: str
    image: str

    class Config:
        orm_mode = True


# ---------- Dependency สำหรับเชื่อมต่อฐานข้อมูล ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- ดึงข้อมูลสุ่มอาหาร ----------
@router.get("/random", response_model=list[RandomFoodOut])
def get_random(db: Session = Depends(get_db)):
    """
    ดึงข้อมูลทั้งหมดจากตาราง random เพื่อใช้สุ่มอาหารในหน้า frontend
    """
    try:
        foods = db.query(Random).all()

        if not foods:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูลในตาราง random")

        return [
            {
                "id": food.random_id,
                "category": food.category,
                "name": food.menu_name,
                "image": food.image,
            }
            for food in foods
        ]

    except Exception as e:
        print("❌ Database error:", e)
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
