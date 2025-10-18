from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, OTPCode
from pydantic import BaseModel
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Forgot Password"])
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

class ForgotRequest(BaseModel):
    new_password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/forgot-password")
def reset_password(data: ForgotRequest, db: Session = Depends(get_db)):
    # ✅ ดึง OTP ล่าสุดที่ถูก verify แล้ว
    otp_entry = (
        db.query(OTPCode)
        .filter(OTPCode.used == True)
        .order_by(OTPCode.created_at.desc())
        .first()
    )

    if not otp_entry:
        raise HTTPException(status_code=400, detail="No verified OTP found")

    # ✅ หา user จากอีเมลที่ OTP ผูกไว้
    user = db.query(User).filter(User.email == otp_entry.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ อัปเดตรหัสผ่านใหม่ (เข้ารหัสก่อนเก็บ)
    user.password = pwd_context.hash(data.new_password)
    db.commit()

    # ✅ ล้างสถานะ OTP เพื่อความปลอดภัย
    otp_entry.used = False
    db.commit()

    return {"message": "Password reset successful"}
