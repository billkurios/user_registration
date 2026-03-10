from abc import ABC, abstractmethod
from domain.schemas.user import User
from typing import Optional


class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        pass
