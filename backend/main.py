from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import requests
import os
from dotenv import load_dotenv
from sqlalchemy import text

from database import SessionLocal
from models import User

load_dotenv()

app = FastAPI()

# ===== ROUTES =====

@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}


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
    # ดึง token และข้อมูลผู้ใช้จาก Google
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
    access_token = token_res.json().get("access_token")

    user_info_res = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={"access_token": access_token},
    )
    user_info = user_info_res.json()

    # บันทึกลงฐานข้อมูล
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


@app.get("/test-db")
def test_database():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  # ✅ ใช้ text() ครอบ SQL
        db.close()
        return {"message": "✅ Database connection successful!"}
    except Exception as e:
        return {"error": f"❌ Database connection failed: {str(e)}"}
