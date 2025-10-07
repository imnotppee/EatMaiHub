from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# โหลดค่าจาก .env
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# URL ที่ใช้กับ Google OAuth
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}

@app.get("/auth/google/login")
def login_with_google():
    auth_url = (
        f"{GOOGLE_AUTH_URL}"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
    )
    return RedirectResponse(auth_url)

@app.get("/auth/google/callback")
def google_callback(request: Request, code: str):
    # 1️⃣ ขอ access token จาก Google
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_res = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    token_json = token_res.json()
    access_token = token_json.get("access_token")

    # 2️⃣ ดึงข้อมูลผู้ใช้จาก Google
    user_info_res = requests.get(
        GOOGLE_USERINFO_URL, params={"access_token": access_token}
    )
    user_info = user_info_res.json()

    # 3️⃣ ส่งกลับผลลัพธ์ (หรือจะ redirect กลับไปหน้า Flet ก็ได้)
    return JSONResponse(content={"user_info": user_info})
