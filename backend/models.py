from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


# -------------------- Review --------------------
class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(TIMESTAMP)


# -------------------- User --------------------
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    zodiac_sign = Column(String(50))
    created_at = Column(TIMESTAMP)


# -------------------- Restaurant --------------------
class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    image_url = Column(Text)
    location = Column(String(255))
    is_featured = Column(Boolean, default=False)
    open_hours = Column(String(100))
    category_id = Column(Integer, ForeignKey("categories.category_id"))


# -------------------- Favorite --------------------
class Favorite(Base):
    __tablename__ = "favorites"

    fav_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    created_at = Column(TIMESTAMP)


# -------------------- History --------------------
class History(Base):
    __tablename__ = "history"

    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    menu_id = Column(Integer)
    viewed_at = Column(TIMESTAMP)
