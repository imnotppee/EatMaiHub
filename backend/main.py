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

# ✅ Component Routes
from component.auth_component import router as auth_router
from component.eat_by_color import register_eat_by_color_routes
from component.highlight_component import register_highlight_routes
from component.sunbae_component import register_sunbae_routes
from component.urban_street_component import register_urban_street_routes
from component.favorite2_component import register_favorite_routes
from component.review2_component import register_review_routes

# ✅ Component อื่นจาก branch origin/main
from component import signup_component, login_component, forgotpass_component, otp_component

# ✅ สร้างตารางอัตโนมัติ (เฉพาะครั้งแรก)
Base.metadata.create_all(bind=engine)

# -------------------------------------------------------
# ⚙️ สร้าง FastAPI Application
# -------------------------------------------------------
app = FastAPI(
    title="EatMaiHub Backend API",
    version="1.0",
    description="🍱 Backend API for EatMaiHub Application"
)

# -------------------------------------------------------
# 🖼️ เสิร์ฟรูปภาพจาก static/images
# -------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(BASE_DIR, "static", "images")

# ✅ เช็กว่ามีโฟลเดอร์จริงก่อน mount (กัน error ตอน Render build)
if os.path.exists(images_path):
    app.mount("/images", StaticFiles(directory=images_path), name="images")

# -------------------------------------------------------
# 🔗 รวม Router ทั้งหมด
# -------------------------------------------------------
# กลุ่มหลัก (มี auth)
app.include_router(auth_router)

# Components ที่ใช้ psycopg2
register_eat_by_color_routes(app, get_conn)
register_highlight_routes(app, get_conn)
register_sunbae_routes(app, get_conn)
register_urban_street_routes(app, get_conn)
register_favorite_routes(app, get_conn)
register_review_routes(app, get_conn)

# Components จาก origin/main (auth/signup/login/otp)
app.include_router(signup_component.router)
app.include_router(login_component.router)
app.include_router(forgotpass_component.router)
app.include_router(otp_component.router)

# -------------------------------------------------------
# 🏠 Root Endpoint
# -------------------------------------------------------
@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}


# -------------------------------------------------------
# 🚀 Entry Point สำหรับ Render
# -------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    # ✅ ใช้ PORT จาก environment variable (Render จะกำหนดให้)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
