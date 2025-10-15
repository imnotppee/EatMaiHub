from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

# -------------------- Database & ORM --------------------
from database import engine, Base, get_conn
from models import (
    User, Restaurant, Category, Menu,
    Review, History, Favorite, ZodiacRecommendation, OTPCode
)

# -------------------- Components --------------------
from component import (
    auth_component,
    categories_component,
    signup_component,
    login_component,
    forgotpass_component,
    otp_component
)

from component.auth_component import router as auth_router
from component.horoscope_component import router as horoscope_router
from component.eat_by_color import register_eat_by_color_routes
from component.highlight_component import register_highlight_routes
from component.sunbae_component import register_sunbae_routes
from component.urban_street_component import register_urban_street_routes
from component.favorite2_component import register_favorite_routes
from component.review2_component import register_review_routes

# -------------------- ⚙️ Database Init --------------------
Base.metadata.create_all(bind=engine)

# -------------------- 🚀 FastAPI Application --------------------
app = FastAPI(
    title="EatMaiHub Backend API",
    version="1.0",
    description="🍱 Backend API for EatMaiHub Application"
)

# -------------------- Static Files --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
images_path = os.path.join(static_path, "images")

# ✅ สร้างโฟลเดอร์ถ้ายังไม่มี เพื่อกัน error ตอน Render build
os.makedirs(images_path, exist_ok=True)

# ✅ เสิร์ฟ static และ images
app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/images", StaticFiles(directory=images_path), name="images")

# -------------------- Register Routers --------------------
# Auth & OAuth
app.include_router(auth_component.router)
app.include_router(auth_router)
app.include_router(horoscope_router)

# Categories
app.include_router(categories_component.router)

# Signup / Login / OTP / Forgot Password
app.include_router(signup_component.router)
app.include_router(login_component.router)
app.include_router(forgotpass_component.router)
app.include_router(otp_component.router)

# Components using get_conn
register_eat_by_color_routes(app, get_conn)
register_highlight_routes(app, get_conn)
register_sunbae_routes(app, get_conn)
register_urban_street_routes(app, get_conn)
register_favorite_routes(app, get_conn)
register_review_routes(app, get_conn)

# -------------------- Root Endpoint --------------------
@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}

# -------------------- Entry Point สำหรับ Render --------------------
if __name__ == "__main__":
    import uvicorn

    # ✅ ใช้ PORT จาก environment variable (Render จะกำหนดให้)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
