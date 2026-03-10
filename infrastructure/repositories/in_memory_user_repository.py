from domain.schemas.user import User
from domain.repositories.user_repository import UserRepository
from typing import Optional, Dict


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.next_id = 1

    async def create_user(self, user: User) -> User:
        user.id = self.next_id
        self.next_id += 1
        self.users[user.email] = user
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return self.users.get(email)
