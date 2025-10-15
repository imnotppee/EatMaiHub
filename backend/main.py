from fastapi import FastAPI
from database import engine, Base
from component import auth_component, favorite_component

# ✅ สร้างตารางอัตโนมัติ
Base.metadata.create_all(bind=engine)

# ✅ สร้าง FastAPI app
app = FastAPI(title="EatMaiHub Backend API", version="1.0")

# ✅ รวมทุก router
app.include_router(auth_component.router)
app.include_router(favorite_component.router)

# ✅ root endpoint
@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}
