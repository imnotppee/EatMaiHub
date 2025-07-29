from fastapi import APIRouter
from .models import User

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Hello from FastAPI!"}

@router.post("/user")
def create_user(user: User):
    return {"username": user.name, "age": user.age}
