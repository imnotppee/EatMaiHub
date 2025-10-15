# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from database import engine, Base, get_conn
from component import auth_component, categories_component
from models import (
    User, Restaurant, Category, Menu,
    Review, History, Favorite, ZodiacRecommendation,
    OTPCode
)
from component.auth_component import router as auth_router
from component.eat_by_color import register_eat_by_color_routes
from component.highlight_component import register_highlight_routes
from component.sunbae_component import register_sunbae_routes
from component.urban_street_component import register_urban_street_routes
from component.favorite2_component import register_favorite_routes
from component.review2_component import register_review_routes
from component.horoscope_component import router as horoscope_router
from component import signup_component, login_component, forgotpass_component, otp_component

# -------------------------------------------------------
# ⚙️ Database init
# -------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ----------------- FastAPI App -----------------
app = FastAPI(
    title="EatMaiHub Backend API",
    version="1.0",
    description="🍱 Backend API for EatMaiHub Application"
)

# ----------------- Mount static images -----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(BASE_DIR, "static", "images")

if not os.path.exists(images_path):
    os.makedirs(images_path, exist_ok=True)

app.mount("/images", StaticFiles(directory=images_path), name="images")

# ----------------- Include Routers -----------------
# Auth & OAuth
app.include_router(auth_component.router)
app.include_router(auth_router)  # legacy router from component.auth_component
app.include_router(horoscope_router)

# Categories
app.include_router(categories_component.router)

# Components using get_conn
register_eat_by_color_routes(app, get_conn)
register_highlight_routes(app, get_conn)
register_sunbae_routes(app, get_conn)
register_urban_street_routes(app, get_conn)
register_favorite_routes(app, get_conn)
register_review_routes(app, get_conn)

# Signup / Login / OTP / Forgot
app.include_router(signup_component.router)
app.include_router(login_component.router)
app.include_router(forgotpass_component.router)
app.include_router(otp_component.router)

# ----------------- Root Endpoint -----------------
@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}

# -------------------------------------------------------
# 🚀 Entry Point
# -------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
