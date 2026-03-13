import asyncpg
import os
from contextlib import asynccontextmanager
from typing import Optional


class DatabasePool:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def create_pool(self):
        """Create the connection pool."""
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL environment variable is not set")

        self.pool = await asyncpg.create_pool(
            db_url,
            min_size=1,
            max_size=10,  # Adjust based on needs
            command_timeout=60,
        )

    async def close_pool(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()

    async def get_connection(self):
        """Get a connection from the pool."""
        if not self.pool:
            await self.create_pool()
        return await self.pool.acquire()

    async def release_connection(self, connection):
        """Release a connection back to the pool."""
        if self.pool:
            await self.pool.release(connection)

    @asynccontextmanager
    async def transaction(self):
        """Provide a connection with an open transaction. Commits on success, rolls back on error."""
        if not self.pool:
            await self.create_pool()
        conn = await self.pool.acquire()
        try:
            async with conn.transaction():
                yield conn
        finally:
            await self.pool.release(conn)

    async def execute(self, query: str, *args):
        """Execute a query."""
        conn = await self.get_connection()
        try:
            result = await conn.execute(query, *args)
            return result
        finally:
            await self.release_connection(conn)

    async def fetch(self, query: str, *args):
        """Fetch multiple rows."""
        conn = await self.get_connection()
        try:
            result = await conn.fetch(query, *args)
            return result
        finally:
            await self.release_connection(conn)

    async def fetchrow(self, query: str, *args):
        """Fetch a single row."""
        conn = await self.get_connection()
        try:
            result = await conn.fetchrow(query, *args)
            return result
        finally:
            await self.release_connection(conn)

    async def fetchval(self, query: str, *args):
        """Fetch a single value."""
        conn = await self.get_connection()
        try:
            result = await conn.fetchval(query, *args)
            return result
        finally:
            await self.release_connection(conn)