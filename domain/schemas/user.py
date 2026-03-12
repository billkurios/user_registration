from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    name: str
    is_active: bool = False

class UserCreate(User):
    password: str