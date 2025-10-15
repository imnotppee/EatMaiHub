from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from pydantic import BaseModel
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Signup"])
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


class UserSignup(BaseModel):
    username: str
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(data: UserSignup, db: Session = Depends(get_db)):
    # ตรวจ email ซ้ำ
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ ป้องกัน password type ผิด
    password_str = str(data.password)

    if len(password_str.strip()) == 0:
        raise HTTPException(status_code=400, detail="Password cannot be empty")

    # ✅ เข้ารหัสอย่างปลอดภัย
    hashed_pwd = pwd_context.hash(password_str[:72])  # bcrypt limit 72 bytes

    new_user = User(
        username=data.username.strip(),
        email=data.email.strip(),
        password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.user_id
    }
