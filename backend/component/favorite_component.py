from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic import BaseModel
from models import Favorite, Restaurant
from datetime import datetime

router = APIRouter(
    prefix="/api/favorites",
    tags=["favorites"]
)

# -------------------- ⚙️ สร้าง Session --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- 📋 Schema --------------------
class FavoriteCreate(BaseModel):
    user_id: int
    restaurant_id: int

# -------------------- 📋 ดึงรายการโปรดทั้งหมด --------------------
@router.get("/")
def get_favorites(db: Session = Depends(get_db)):
    try:
        favorites = (
            db.query(
                Favorite.fav_id,
                Favorite.user_id,
                Restaurant.name,
                Restaurant.description,
                Restaurant.image_url,
                Restaurant.location
            )
            .join(Restaurant, Favorite.restaurant_id == Restaurant.id)  # ✅ join ตรงกับ DB
            .order_by(Favorite.fav_id.asc())
            .all()
        )

        return [
            {
                "fav_id": f.fav_id,
                "user_id": f.user_id,
                "name": f.name,
                "description": f.description,
                "image": f.image_url,
                "location": f.location,
            }
            for f in favorites
        ]
    except Exception as e:
        print("❌ ERROR get_favorites:", e)
        raise HTTPException(status_code=500, detail=str(e))


# -------------------- ❤️ เพิ่มรายการโปรด --------------------
@router.post("/")
def add_favorite(data: FavoriteCreate, db: Session = Depends(get_db)):
    try:
        new_fav = Favorite(
            user_id=data.user_id,
            restaurant_id=data.restaurant_id,
            created_at=datetime.now()
        )
        db.add(new_fav)
        db.commit()
        db.refresh(new_fav)
        return {"message": "Favorite added successfully!", "fav_id": new_fav.fav_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# -------------------- 💔 ลบรายการโปรด --------------------
@router.delete("/{fav_id}")
def delete_favorite(fav_id: int, db: Session = Depends(get_db)):
    try:
        fav = db.query(Favorite).filter(Favorite.fav_id == fav_id).first()
        if not fav:
            raise HTTPException(status_code=404, detail="Favorite not found")

        db.delete(fav)
        db.commit()
        return {"message": "Favorite removed successfully!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
