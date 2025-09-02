from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from schemas import UserOut, UserProfileUpdate

router = APIRouter(prefix="/me", tags=["member"])

def get_current_user_id():
    return 1

@router.get("/profile", response_model=UserOut)
def get_profile(user_id: int = Depends(get_current_user_id)):
    # TODO: SELECT user by id
    return UserOut(id=user_id, email="demo@example.com", name="Demo")

@router.patch("/profile", response_model=UserOut)
def update_profile(payload: UserProfileUpdate, user_id: int = Depends(get_current_user_id)):
    # TODO: UPDATE user profile
    return UserOut(id=user_id, email="demo@example.com", name=payload.name or "Demo")

@router.get("/history", response_model=List[Dict[str, Any]])
def usage_history(user_id: int = Depends(get_current_user_id)):
    # TODO: คืนประวัติการใช้งาน (ค้นหา/รีวิว/สั่งซื้อ ฯลฯ)
    return []
