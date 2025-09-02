from fastapi import APIRouter, HTTPException
from schemas import UserRegister, UserLogin, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(payload: UserRegister):
    # TODO: Recheck email, hash password, save user
    return UserOut(id=1, email=payload.email, name=payload.name)

@router.post("/login", response_model=UserOut)
def login(payload: UserLogin):
    # TODO: verify password, issue token (JWT) -> Return profile
    # Return access_token
    if payload.email == "demo@example.com":
        return UserOut(id=1, email=payload.email, name="Demo")
    raise HTTPException(status_code=401, detail="invalid credentials")
