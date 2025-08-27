from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas

# Users
def create_user(db: Session, data: schemas.UserCreate):
    obj = models.User(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj

def list_users(db: Session):
    return db.execute(select(models.User)).scalars().all()

# Restaurants
def create_restaurant(db: Session, data: schemas.RestaurantCreate):
    obj = models.Restaurant(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj

def list_restaurants(db: Session, category: str | None = None):
    stmt = select(models.Restaurant)
    if category: stmt = stmt.where(models.Restaurant.category == category)
    return db.execute(stmt).scalars().all()

# Menus
def create_menu(db: Session, data: schemas.MenuCreate):
    obj = models.Menu(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj

def list_menus_by_restaurant(db: Session, restaurant_id: int):
    stmt = select(models.Menu).where(models.Menu.restaurant_id == restaurant_id)
    return db.execute(stmt).scalars().all()

# Reviews
def create_review(db: Session, data: schemas.ReviewCreate):
    obj = models.Review(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj

def list_reviews_by_restaurant(db: Session, restaurant_id: int):
    stmt = select(models.Review).where(models.Review.restaurant_id == restaurant_id)
    return db.execute(stmt).scalars().all()
