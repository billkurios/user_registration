import logging
from domain.schemas.user import User, UserCreate
from domain.repositories.user_repository import UserRepository
from infrastructure.database_pool import DatabasePool
from typing import Optional, List


logger = logging.getLogger(__name__)


class DatabaseUserRepository(UserRepository):
    def __init__(self, db_pool: DatabasePool):
        self.db_pool = db_pool

    async def create_user(self, user: UserCreate) -> User:
        """Create a new user in the database."""
        logger.debug("create_user query start", extra={"email": user.email, "name": user.name})
        query = """
            INSERT INTO users (email, "user", password)
            VALUES ($1, $2, $3)
            RETURNING id
        """
        user_id = await self.db_pool.fetchval(query, user.email, user.name, user.password)
        logger.info("create_user query success", extra={"email": user.email, "user_id": user_id})
        return User(email=user.email, name=user.name, id=user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email from the database."""
        logger.debug("get_user_by_email query start", extra={"email": email})
        query = """
            SELECT id, email, "user" AS name, is_active
            FROM users
            WHERE email = $1
        """
        row = await self.db_pool.fetchrow(query, email)
        logger.debug(f"get_user_by_email query result {row}", extra={"email": email, "found": bool(row)})
        return User(**row) if row else None

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID from the database."""
        query = """
            SELECT id, email, "user" AS name, is_active
            FROM users
            WHERE id = $1
        """
        row = await self.db_pool.fetchrow(query, user_id)
        return User(**row) if row else None

    async def get_all_users(self) -> List[User]:
        """Retrieve all users from the database."""
        query = """
            SELECT id, email, "user" AS name, is_active
            FROM users
            ORDER BY id
        """
        rows = await self.db_pool.fetch(query)
        return [User(**row) for row in rows]

    async def update_user(self, user_id: int, updated_user: User) -> Optional[User]:
        """Update an existing user in the database."""
        query = """
            UPDATE users
            SET email = $1, "user" = $2
            WHERE id = $3
            RETURNING id, email, "user" AS name
        """
        row = await self.db_pool.fetchrow(
            query,
            updated_user.email,
            updated_user.name,
            user_id
        )
        return User(**row, id=int(row["id"])) if row else None

    async def delete_user(self, user_id: int) -> bool:
        """Delete a user from the database."""
        query = """
            DELETE FROM users
            WHERE id = $1
            RETURNING id
        """
        result = await self.db_pool.fetchval(query, user_id)
        return result is not None
