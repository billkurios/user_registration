from domain.schemas.user import User
from domain.repositories.user_repository import UserRepository
from typing import Optional


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, email: str, name: str, password: str) -> User:
        # Check if user exists
        existing = await self.user_repo.get_user_by_email(email)
        if existing:
            raise ValueError("User already exists")
        user = User(
            email=email, name=name, password=password
        )  # Hash password in real app
        return await self.user_repo.create_user(user)
