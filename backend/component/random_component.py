from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic import BaseModel
from models import Random

router = APIRouter(prefix="/api", tags=["Random Food"])

class RandomFoodOut(BaseModel):
    id: int
    category: str
    name: str
    image: str

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/random")
def get_random(db: Session = Depends(get_db)):
    try:
        print("📦 ใช้ฐานข้อมูล:", db.bind.url)

        foods = db.query(Random).all()
        if not foods:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูลในตาราง random")

        data = [
            {
                "id": food.random_id,
                "category": food.category,
                "name": food.menu_name,
                "image": food.image,
            }
            for food in foods
        ]

        return JSONResponse(content=jsonable_encoder(data))  # ✅ รองรับภาษาไทย

    except Exception as e:
        print("❌ Database error:", e)
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
