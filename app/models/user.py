# app/models/user.py

from pydantic import BaseModel
import datetime

class Badge(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True

class UserBadge(BaseModel):
    awarded_date: datetime.datetime
    badge: Badge

    class Config:
        from_attributes = True
        
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# --- ADD THIS CLASS TO THE END OF THE FILE ---

class LeaderboardUser(BaseModel):
    id: int
    username: str
    total_points: int

    class Config:
        from_attributes = True