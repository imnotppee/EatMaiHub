from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

# -------------------- 🗄️ Database & ORM --------------------
from database import engine, Base, get_conn

# โหลด Models ทั้งหมดให้ SQLAlchemy สร้างตาราง
from models import (
    User, Restaurant, Category, Menu,
    Review, History, Favorite, ZodiacRecommendation,
    OTPCode
)

# -------------------- 🔗 Components --------------------
# from component.auth_component import router as auth_router
# from component.random_component import router as random_router
# from component.eat_by_color import register_eat_by_color_routes
# from component.highlight_component import register_highlight_routes
# from component.sunbae_component import register_sunbae_routes
# from component.urban_street_component import register_urban_street_routes
# from component.favorite2_component import register_favorite_routes
from component.review2_component import register_review_routes  # ✅ ใช้งานรีวิว

# -------------------- ⚙️ Database init --------------------
Base.metadata.create_all(bind=engine)

# -------------------- 🚀 FastAPI Application --------------------
app = FastAPI(
    title="EatMaiHub Backend API",
    version="1.0",
    description="Backend API for EatMaiHub Application"
)

# -------------------- 🖼️ Static Files --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
images_path = os.path.join(static_path, "images")

# ✅ mount ทั้งโฟลเดอร์ static (รองรับรูป .jpg, .png, .webp)
app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/images", StaticFiles(directory=images_path), name="images")

# -------------------- 🔌 Register Routers --------------------
# app.include_router(auth_router)
# app.include_router(random_router)
# register_eat_by_color_routes(app, get_conn)
# register_highlight_routes(app, get_conn)
# register_sunbae_routes(app, get_conn)
# register_urban_street_routes(app, get_conn)
# register_favorite_routes(app, get_conn)

# ✅ เปิดใช้งานเส้นทางรีวิว (Review API)
register_review_routes(app, get_conn)

# -------------------- 🌐 Root Endpoint --------------------
@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}

# -------------------- 🏁 Entry Point --------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
