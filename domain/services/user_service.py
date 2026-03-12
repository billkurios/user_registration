import logging
from domain.schemas.user import User, UserCreate
from domain.repositories.user_repository import UserRepository
from typing import Optional


logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, email: str, name: str, password: str) -> User:
        logger.debug("register_user called", extra={"email": email, "name": name})
        # Check if user exists
        existing = await self.user_repo.get_user_by_email(email)
        if existing:
            logger.info("register_user rejected: user already exists", extra={"email": email})
            raise ValueError("User already exists")
        user = UserCreate(
            email=email, name=name, password=password
        )  # Hash password in real app
        response = await self.user_repo.create_user(user)
        logger.info("register_user succeeded", extra={"email": response.email, "user_id": response.id})
        return response
