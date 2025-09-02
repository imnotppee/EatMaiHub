from fastapi import APIRouter
from schemas import MenuOut

router = APIRouter(prefix="/random", tags=["random"])

@router.get("/menu", response_model=MenuOut)
def random_menu():
    # TODO: ดึงจาก DB แบบสุ่มตามเงื่อนไข (ราคา/แท็ก/ร้านเปิดอยู่)
    return MenuOut(id=1, name="ข้าวกะเพราไข่ดาว", price=55.0, image_url=None, restaurant_id=10)