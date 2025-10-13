from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import os, requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/google/login")
def google_login():
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={os.getenv('GOOGLE_CLIENT_ID')}"
        f"&redirect_uri={os.getenv('REDIRECT_URI')}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
    )
    return RedirectResponse(auth_url)


@router.get("/google/callback")
def google_callback(request: Request, code: str):
    try:
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

        user_info_res = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            params={"access_token": access_token},
        )
        user_info = user_info_res.json()

        db: Session = SessionLocal()
        user = db.query(User).filter(User.email == user_info["email"]).first()

        if not user:
            new_user = User(username=user_info["name"], email=user_info["email"], password="")
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            db.close()
            return JSONResponse(content={"message": "🎉 New user added!", "user": user_info})

        db.close()
        return JSONResponse(content={"message": "👋 Welcome back!", "user": user_info})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OAuth failed: {str(e)}")
