from abc import ABC, abstractmethod
from domain.schemas.user import User
from typing import Optional, List


class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    async def update_user(self, user_id: int, updated_user: User) -> Optional[User]:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        pass
