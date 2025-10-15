from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

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


class Restaurant(Base):
    __tablename__ = "restaurants"

    restaurant_id = Column(Integer, primary_key=True, index=True)
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


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    icon_url = Column(Text)

    restaurants = relationship("Restaurant", backref="category")


class Menu(Base):
    __tablename__ = "menus"

    menu_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    menu_name = Column(String(255))
    price = Column(DECIMAL(10, 2))
    image_url = Column(Text)
    color_of_day = Column(String(50))

    restaurant = relationship("Restaurant", back_populates="menus")
    history = relationship("History", back_populates="menu")


class ZodiacRecommendation(Base):
    __tablename__ = "zodiac_recommendations"

    zodiac_id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String(20))
    recommended_menu = Column(String(255))
    image_url = Column(Text)


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")


class History(Base):
    __tablename__ = "history"

    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    menu_id = Column(Integer, ForeignKey("menus.menu_id"))
    viewed_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="history")
    restaurant = relationship("Restaurant", back_populates="history")
    menu = relationship("Menu", back_populates="history")


class Favorite(Base):
    __tablename__ = "favorites"

    fav_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))
    created_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="favorites")
    restaurant = relationship("Restaurant", back_populates="favorites")

class Random(Base):
    __tablename__ = "random"

    random_id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    menu_name = Column(String)
    image = Column(String)