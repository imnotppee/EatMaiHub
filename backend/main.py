from fastapi import FastAPI
from database import engine, Base
from component import auth_component, horoscope_component

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EatMaiHub Backend API", version="1.0")

# รวม router
app.include_router(auth_component.router)
app.include_router(horoscope_component.router)

@app.get("/")
def home():
    return {"message": "EatMaiHub Backend is running 🚀"}
