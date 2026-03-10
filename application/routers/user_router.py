from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from domain.services.user_service import UserService
from domain.schemas.user import User

router = APIRouter()


class UserCreateRequest(BaseModel):
    email: str
    name: str
    password: str


# Dependency injection would be handled by container
# For simplicity, we'll inject directly in main.py


@router.post("/register", response_model=User)
async def register_user(
    request: UserCreateRequest, user_service: UserService = Depends()
):
    try:
        user = await user_service.register_user(
            request.email, request.name, request.password
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
