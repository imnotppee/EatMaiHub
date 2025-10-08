from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
import requests
import os
from dotenv import load_dotenv

# ==== LOCAL IMPORTS ====
from database import SessionLocal, engine
from models import Base, User

# โหลดค่า environment variables
load_dotenv()

# ==== INITIALIZE APP ====
app = FastAPI()

# ✅ สร้างตารางอัตโนมัติ ถ้ายังไม่มี
Base.metadata.create_all(bind=engine)


# ==== ROUTES ====

@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}


# ------------------ GOOGLE OAUTH ------------------

@app.get("/auth/google/login")
def login_with_google():
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={os.getenv('GOOGLE_CLIENT_ID')}"
        f"&redirect_uri={os.getenv('REDIRECT_URI')}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
    )
    return RedirectResponse(auth_url)


@app.get("/auth/google/callback")
def google_callback(request: Request, code: str):
    # 1️⃣ ขอ access token จาก Google
    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": os.getenv("REDIRECT_URI"),
            "grant_type": "authorization_code",
        },
    )

    token_json = token_res.json()
    access_token = token_json.get("access_token")

    # 2️⃣ ดึงข้อมูลผู้ใช้จาก Google
    user_info_res = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={"access_token": access_token},
    )
    user_info = user_info_res.json()

    # 3️⃣ เชื่อมฐานข้อมูล
    db = SessionLocal()
    existing_user = db.query(User).filter(User.google_id == user_info["id"]).first()

    if not existing_user:
        new_user = User(
            google_id=user_info["id"],
            name=user_info["name"],
            email=user_info["email"],
            picture=user_info["picture"]
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
        return JSONResponse(content={"message": "🎉 New user added!", "user": user_info})
    else:
        db.close()
        return JSONResponse(content={"message": "👋 Welcome back!", "user": user_info})


# ------------------ TEST DATABASE ------------------

@app.get("/test-db")
def test_database():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"message": "✅ Database connection successful!"}
    except Exception as e:
        return {"error": f"❌ Database connection failed: {str(e)}"}


# ------------------ CRUD TEST ------------------

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str


@app.post("/add-user")
def add_user(user: UserCreate):
    db = SessionLocal()
    new_user = User(username=user.username, password=user.password, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return {"message": "✅ User added successfully!", "user": {"id": new_user.id, "username": new_user.username}}


@app.get("/get-users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return {"users": [{"id": u.id, "username": u.username, "email": u.email} for u in users]}


@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        db.close()
        return {"message": "🗑️ User deleted!"}
    db.close()
    return {"error": "❌ User not found"}

