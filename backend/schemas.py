from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    email: str
    name: str

class UserOut(UserCreate):
    id: int
    class Config: from_attributes = True

class RestaurantCreate(BaseModel):
    name: str
    category: Optional[str] = "Thai"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact: Optional[str] = None

class RestaurantOut(RestaurantCreate):
    id: int
    class Config: from_attributes = True

class MenuCreate(BaseModel):
    restaurant_id: int
    name: str
    price: float = Field(ge=0)
    tag: Optional[str] = None

class MenuOut(MenuCreate):
    id: int
    class Config: from_attributes = True

class ReviewCreate(BaseModel):
    restaurant_id: int
    user_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = ""

class ReviewOut(ReviewCreate):
    id: int
    class Config: from_attributes = True
