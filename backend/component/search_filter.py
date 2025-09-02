from fastapi import APIRouter
from typing import List
from schemas import SearchQuery, RestaurantOut, MenuOut

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/restaurants", response_model=List[RestaurantOut])
def search_restaurants(q: SearchQuery):
    # TODO: WHERE keyword/category/area + ORDER BY sort_by
    return []

@router.post("/menus", response_model=List[MenuOut])
def search_menus(q: SearchQuery):
    # TODO: WHERE keyword/price/rating + ORDER BY
    return []
