from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # ✅ เพิ่มบรรทัดนี้
from database import engine, Base
from component import random_component

# ✅ Import models ทั้งหมด เพื่อให้ SQLAlchemy รู้จักทุกตารางก่อนสร้าง
from models import (
    User, Restaurant, Category, Menu,
    Review, History, Favorite, ZodiacRecommendation,
    OTPCode
)

# ✅ สร้างตารางอัตโนมัติ — ใช้ create_all() (ไม่ลบข้อมูลเก่า)
# ถ้าตารางมีอยู่แล้ว SQLAlchemy จะไม่แตะต้องข้อมูล
Base.metadata.create_all(bind=engine)

# ✅ สร้าง FastAPI app
app = FastAPI(title="EatMaiHub Backend API", version="1.0")

# ✅ Mount static files (ใช้เส้นทาง /static/photo/)
# หมายเหตุ: ปรับ path ให้ตรงกับโครงสร้างโฟลเดอร์จริงของคุณ
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# ✅ รวม router ต่าง ๆ
# app.include_router(auth_component.router)
# app.include_router(signup_component.router)
# app.include_router(login_component.router)
# app.include_router(forgotpass_component.router)
# app.include_router(otp_component.router)
app.include_router(random_component.router)

# ✅ root endpoint
@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}
