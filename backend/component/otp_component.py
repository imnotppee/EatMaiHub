# backend/component/otp_component.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from email.message import EmailMessage
import secrets, hmac, hashlib, smtplib
import os

from database import get_db
from models import User, OTPCode
from config import (
    MAIL_FROM, SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS,
    OTP_SECRET, OTP_EXP_MINUTES
)

router = APIRouter(prefix="/auth", tags=["OTP Verification"])

# ------------------------- Helper Functions -------------------------
def generate_otp(length=6):
    """สร้างเลขสุ่ม 6 หลัก"""
    return str(secrets.randbelow(10**length)).zfill(length)

def hash_otp(otp_plain: str, salt: str) -> str:
    """เข้ารหัส OTP ด้วย HMAC SHA256"""
    return hmac.new(OTP_SECRET.encode(), f"{otp_plain}|{salt}".encode(), hashlib.sha256).hexdigest()

def send_email(to_email: str, subject: str, body: str):
    """ส่งอีเมลผ่าน Gmail SMTP"""
    msg = EmailMessage()
    msg["From"] = MAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)

# ------------------------- Request Models -------------------------
class RequestOtpIn(BaseModel):
    email: EmailStr

class VerifyOtpIn(BaseModel):
    email: EmailStr
    otp: str

# ------------------------- Routes -------------------------
@router.post("/request-otp")
def request_otp(payload: RequestOtpIn, db: Session = Depends(get_db)):
    """ขอรหัส OTP ไปที่อีเมล"""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="ไม่พบบัญชีผู้ใช้ที่ใช้อีเมลนี้")

    # ป้องกัน spam: ขอ OTP ถี่เกินไป
    recent = (
        db.query(OTPCode)
        .filter(OTPCode.email == payload.email)
        .order_by(OTPCode.created_at.desc())
        .first()
    )
    if recent and (datetime.utcnow() - recent.created_at).total_seconds() < 60:
        raise HTTPException(status_code=429, detail="กรุณารอสักครู่ก่อนขอรหัสใหม่")

    otp_plain = generate_otp(6)
    salt = f"{user.user_id}-{int(datetime.utcnow().timestamp())}"
    otp_hash = hash_otp(otp_plain, salt)
    expires = datetime.utcnow() + timedelta(minutes=OTP_EXP_MINUTES)

    otp_row = OTPCode(
        user_id=user.user_id,
        email=user.email,
        otp_hash=f"{otp_hash}:{salt}",
        created_at=datetime.utcnow(),
        expires_at=expires,
        attempts=0,
        used=False,
    )
    db.add(otp_row)
    db.commit()

    subject = "รหัสยืนยัน (OTP) สำหรับ EatMaiHub"
    body = (
        f"รหัส OTP ของคุณคือ: {otp_plain}\n"
        f"ใช้ได้ภายใน {OTP_EXP_MINUTES} นาที\n"
        "ห้ามเปิดเผยรหัสนี้ให้ผู้อื่นรู้เด็ดขาด"
    )

    try:
        send_email(user.email, subject, body)
    except Exception as e:
        db.delete(otp_row)
        db.commit()
        raise HTTPException(status_code=500, detail=f"ไม่สามารถส่งอีเมลได้: {e}")

    return {"message": "ส่งรหัส OTP ไปยังอีเมลแล้ว"}

@router.post("/verify-otp")
def verify_otp(payload: VerifyOtpIn, db: Session = Depends(get_db)):
    """ตรวจสอบ OTP ที่ผู้ใช้กรอก"""
    otp_row = (
        db.query(OTPCode)
        .filter(OTPCode.email == payload.email, OTPCode.used == False)
        .order_by(OTPCode.created_at.desc())
        .first()
    )
    if not otp_row:
        raise HTTPException(status_code=404, detail="ไม่พบรหัส OTP")

    if datetime.utcnow() > otp_row.expires_at:
        raise HTTPException(status_code=400, detail="รหัส OTP หมดอายุแล้ว")

    if otp_row.attempts >= 5:
        raise HTTPException(status_code=429, detail="กรอกรหัสผิดเกินจำนวนครั้งที่กำหนด")

    stored_hash, salt = otp_row.otp_hash.split(":", 1)
    candidate = hash_otp(payload.otp, salt)

    if not hmac.compare_digest(candidate, stored_hash):
        otp_row.attempts += 1
        db.commit()
        raise HTTPException(status_code=400, detail="รหัส OTP ไม่ถูกต้อง")

    otp_row.used = True
    db.commit()
    return {"message": "ยืนยัน OTP สำเร็จ ✅"}
