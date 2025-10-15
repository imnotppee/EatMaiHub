from fastapi import FastAPI
from database import engine, Base, get_conn
from fastapi.staticfiles import StaticFiles
import os

# 🧩 นำเข้า Component ทั้งหมด
from component.auth_component import router as auth_router
from component.eat_by_color import register_eat_by_color_routes
from component.highlight_component import register_highlight_routes
from component.sunbae_component import register_sunbae_routes
from component.urban_street_component import register_urban_street_routes
from component.favorite2_component import register_favorite_routes
from component.review2_component import register_review_routes


# ✅ สร้างตารางอัตโนมัติ (เฉพาะเมื่อใช้ SQLAlchemy ORM)
Base.metadata.create_all(bind=engine)

# ✅ สร้าง FastAPI app
app = FastAPI(
    title="EatMaiHub Backend API",
    version="1.0",
    description="🍱 Backend API for EatMaiHub Application"
)

# ✅ เสิร์ฟรูปภาพจากโฟลเดอร์ static/images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(BASE_DIR, "static", "images")
app.mount("/images", StaticFiles(directory=images_path), name="images")

# ✅ รวม router ทั้งหมด
app.include_router(auth_router)
register_eat_by_color_routes(app, get_conn)
register_highlight_routes(app, get_conn)
register_sunbae_routes(app, get_conn)
register_urban_street_routes(app, get_conn)
register_favorite_routes(app, get_conn)
register_review_routes(app, get_conn)


# ✅ root endpoint
@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}


# ✅ ใช้ตอนรันโดยตรง (ไม่จำเป็นตอนรันผ่าน uvicorn)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
