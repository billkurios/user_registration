from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    name: str
    password: str  # In real app, hash this

    class Config:
        from_attributes = True