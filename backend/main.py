# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

# ✅ Database & ORM
from database import engine, Base, get_conn

# ✅ โหลด Models ทั้งหมดให้ SQLAlchemy สร้างตาราง
from models import (
    User, Restaurant, Category, Menu,
    Review, History, Favorite, ZodiacRecommendation,
    OTPCode
)

# ✅ Component Routers
# from component.auth_component import router as auth_router
from component.random_component import router as random_router
# from component.eat_by_color import register_eat_by_color_routes
# from component.highlight_component import register_highlight_routes
# from component.sunbae_component import register_sunbae_routes
# from component.urban_street_component import register_urban_street_routes
# from component.favorite2_component import register_favorite_routes
# from component.review2_component import register_review_routes

# ✅ Components จาก origin/main (auth/signup/login/otp)
# from component import signup_component, login_component, forgotpass_component, otp_component

# -------------------------------------------------------
# ⚙️ Database init
# -------------------------------------------------------
Base.metadata.create_all(bind=engine)

# -------------------------------------------------------
# ⚙️ FastAPI Application
# -------------------------------------------------------
app = FastAPI(
    title="EatMaiHub Backend API",
    version="1.0",
    description="Backend API for EatMaiHub Application"
)

# -------------------------------------------------------
# 🖼️ เสิร์ฟรูปภาพจาก backend/static/images
# -------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ เสิร์ฟโฟลเดอร์ static ทั้งหมด (รวม images, .jpg, .jpeg, .webp)
static_path = os.path.join(BASE_DIR, "static")
images_path = os.path.join(static_path, "images")

# ✅ mount static หลัก (รองรับ .jpg, .jpeg, .png, .webp)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# ✅ mount เฉพาะโฟลเดอร์ images เพิ่ม (เพื่อความเข้ากันได้กับโค้ดเก่า)
app.mount("/images", StaticFiles(directory=images_path), name="images")

# -------------------------------------------------------
# 🔗 รวม Router ทั้งหมด
# -------------------------------------------------------
# app.include_router(auth_router)
app.include_router(random_router)
# app.include_router(signup_component.router)
# app.include_router(login_component.router)
# app.include_router(forgotpass_component.router)
# app.include_router(otp_component.router)

# Components ที่ใช้ psycopg2 (ผ่าน get_conn)
# register_eat_by_color_routes(app, get_conn)
# register_highlight_routes(app, get_conn)
# register_sunbae_routes(app, get_conn)
# register_urban_street_routes(app, get_conn)
# register_favorite_routes(app, get_conn)
# register_review_routes(app, get_conn)

# -------------------------------------------------------
# 🏠 Root Endpoint
# -------------------------------------------------------
@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}

# -------------------------------------------------------
# 🚀 Entry Point
# -------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
