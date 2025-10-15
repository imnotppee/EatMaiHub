from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

# ========================= USERS =========================
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    zodiac_sign = Column(String(50))
    created_at = Column(TIMESTAMP)

    reviews = relationship("Review", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
    history = relationship("History", back_populates="user")
    otp_codes = relationship("OTPCode", back_populates="user", cascade="all, delete-orphan")


# ========================= RESTAURANTS =========================
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

    menus = relationship("Menu", back_populates="restaurant")
    reviews = relationship("Review", back_populates="restaurant")
    favorites = relationship("Favorite", back_populates="restaurant")
    history = relationship("History", back_populates="restaurant")


# ========================= CATEGORIES =========================
class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    icon_url = Column(Text)

    restaurants = relationship("Restaurant", backref="category")


# ========================= MENUS =========================
class Menu(Base):
    __tablename__ = "menus"

    menu_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    menu_name = Column(String(255))
    price = Column(DECIMAL(10, 2))
    image_url = Column(Text)
    color_of_day = Column(String(50))

    restaurant = relationship("Restaurant", back_populates="menus")
    history = relationship("History", back_populates="menu")


# ========================= ZODIAC =========================
class ZodiacRecommendation(Base):
    __tablename__ = "zodiac_recommendations"

    zodiac_id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String(20))
    recommended_menu = Column(String(255))
    image_url = Column(Text)


# ========================= REVIEWS =========================
class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")


# ========================= HISTORY =========================
class History(Base):
    __tablename__ = "history"

    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    menu_id = Column(Integer, ForeignKey("menus.menu_id"))
    viewed_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="history")
    restaurant = relationship("Restaurant", back_populates="history")
    menu = relationship("Menu", back_populates="history")


# ========================= FAVORITES =========================
class Favorite(Base):
    __tablename__ = "favorites"

    fav_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="favorites")
    restaurant = relationship("Restaurant", back_populates="favorites")


# ========================= OTP CODES =========================
class OTPCode(Base):
    """
    เก็บรหัส OTP สำหรับยืนยันตัวตน/รีเซ็ตรหัสผ่าน
    - otp_hash เก็บ hash ของรหัส (hash:salt)
    - expires_at เวลาหมดอายุ
    - attempts จำนวนครั้งที่พยายามใส่
    - used ใช้แล้วหรือยัง
    """
    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    email = Column(String(255), nullable=False)
    otp_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP)
    expires_at = Column(TIMESTAMP)
    attempts = Column(Integer, default=0)
    used = Column(Boolean, default=False)

    user = relationship("User", back_populates="otp_codes")
