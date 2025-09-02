from fastapi import APIRouter
from typing import List
from schemas import NearbyQuery, RestaurantOut

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/nearby", response_model=List[RestaurantOut])
def nearby(q: NearbyQuery):
    # TODO: คำนวณระยะทาง Haversine + ดึงร้านที่อยู่ใน radius_km
    return [
        RestaurantOut(id=10, name="ก๋วยเตี๋ยวป้าหวาน", address="บางกะปิ", distance_km=0.4, rating=4.5, lat=q.lat, lng=q.lng, categories=["thai"]),
    ]

@router.get("/categories/{category}", response_model=List[RestaurantOut])
def by_category(category: str):
    # TODO: ค้นหาร้านตามประเภท เช่น thai/japanese/fastfood
    return []
