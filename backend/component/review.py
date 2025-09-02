from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas import ReviewCreate, ReviewOut

router = APIRouter(prefix="/reviews", tags=["reviews"])

# สมมติ auth แล้วได้ user_id
def get_current_user_id():
    return 1

@router.post("/", response_model=ReviewOut)
def create_review(payload: ReviewCreate, user_id: int = Depends(get_current_user_id)):
    if payload.rating < 1 or payload.rating > 5:
        raise HTTPException(status_code=400, detail="rating must be 1-5")
    # TODO: บันทึก DB
    return ReviewOut(id=1, user_id=user_id, **payload.model_dump())

@router.get("/restaurant/{restaurant_id}", response_model=List[ReviewOut])
def list_reviews(restaurant_id: int):
    # TODO: SELECT reviews ของร้าน
    return []
