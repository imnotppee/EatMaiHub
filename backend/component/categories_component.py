from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, relationship, declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# ----------------- Load environment variables -----------------
load_dotenv()

# ----------------- Database Setup -----------------
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ----------------- Models -----------------
class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    icon_url = Column(Text)

    restaurants = relationship("Restaurant", backref="category")


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    is_featured = Column(Boolean, default=False)
    open_hours = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"))

# ----------------- Dependency -----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------- Router -----------------
router = APIRouter(prefix="/api", tags=["categories"])

@router.get("/restaurants")
def get_restaurants(db: Session = Depends(get_db)):
    try:
        restaurants = db.query(Restaurant).all()
        result = []

        for r in restaurants:
            category_name = r.category.category_name if getattr(r, "category", None) else None

            if not category_name:
                category_name = {
                    1: "fast_foods",
                    2: "japan_foods",
                    3: "thai_foods"
                }.get(r.category_id)

            restaurant_item = {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "image_url": r.image_url,
                "location": r.location,
                "is_featured": r.is_featured,
                "open_hours": r.open_hours,
                "category_name": category_name
            }
            result.append(restaurant_item)

        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------- App -----------------
app = FastAPI()
app.include_router(router)
