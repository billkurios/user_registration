import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import os
from infrastructure.database_pool import DatabasePool


class TestDatabasePool:
    """
    Unit tests for the DatabasePool helper class.

    The test scenarios covered by this class include:

    * **create_pool_success** – ensures `create_pool` reads DATABASE_URL from
      the environment, calls `asyncpg.create_pool` with the expected
      parameters, and stores the resulting pool.
    * **create_pool_no_env_var** – verifies that the method raises a
      ValueError when the environment variable is missing.
    * **close_pool_with_pool** – closing an already-initialized pool should
      call the pool's `close` method.
    * **close_pool_no_pool** – closing when no pool exists should silently
      return without error.
    * **get_connection_creates_pool_if_none** – requesting a connection when no
      pool exists triggers pool creation and then acquires a connection.
    * **get_connection_existing_pool** – acquiring from an existing pool only
      uses `acquire` on the current pool.
    * **release_connection_with_pool** – releasing a connection should call
      `release` on the pool when available.
    * **release_connection_no_pool** – attempting to release without a pool
      should be a no-op.
    * **execute/fetch/fetchrow/fetchval** – verify that each query helper
      method acquires a connection, performs the correct call, and releases the
      connection afterward, returning the underlying result.
    """

    @pytest.fixture
    def db_pool(self):
        """Fixture to create a fresh DatabasePool instance."""
        return DatabasePool()

    @pytest.fixture
    def mock_pool(self):
        """Fixture for a mock asyncpg pool."""
        pool = AsyncMock()
        pool.close = AsyncMock()
        pool.acquire = AsyncMock()
        pool.release = AsyncMock()
        return pool

    @patch.dict(os.environ, {"DATABASE_URL": "postgresql://test:test@localhost/testdb"})
    @patch('infrastructure.database_pool.asyncpg.create_pool')
    @pytest.mark.asyncio
    async def test_create_pool_success(self, mock_create_pool, db_pool, mock_pool):
        """Test successful pool creation."""
        mock_create_pool.return_value = mock_pool

        await db_pool.create_pool()

        mock_create_pool.assert_called_once_with(
            "postgresql://test:test@localhost/testdb",
            min_size=1,
            max_size=10,
            command_timeout=60,
        )
        assert db_pool.pool == mock_pool

    @patch.dict(os.environ, {}, clear=True)
    @pytest.mark.asyncio
    async def test_create_pool_no_env_var(self, db_pool):
        """Test pool creation fails without DATABASE_URL."""
        with pytest.raises(ValueError, match="DATABASE_URL environment variable is not set"):
            await db_pool.create_pool()

    @pytest.mark.asyncio
    async def test_close_pool_with_pool(self, db_pool, mock_pool):
        """Test closing an existing pool."""
        db_pool.pool = mock_pool

        await db_pool.close_pool()

        mock_pool.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_pool_no_pool(self, db_pool):
        """Test closing when no pool exists."""
        db_pool.pool = None

        await db_pool.close_pool()

        # Should not raise any error

    @patch('infrastructure.database_pool.asyncpg.create_pool')
    @pytest.mark.asyncio
    async def test_get_connection_creates_pool_if_none(self, mock_create_pool, db_pool, mock_pool):
        """Test get_connection creates pool if not exists."""
        mock_create_pool.return_value = mock_pool
        mock_pool.acquire.return_value = AsyncMock()
        db_pool.pool = None

        with patch.dict(os.environ, {"DATABASE_URL": "postgresql://test"}):
            conn = await db_pool.get_connection()

        mock_create_pool.assert_called_once()
        mock_pool.acquire.assert_called_once()
        assert conn == mock_pool.acquire.return_value

    @pytest.mark.asyncio
    async def test_get_connection_existing_pool(self, db_pool, mock_pool):
        """Test get_connection uses existing pool."""
        db_pool.pool = mock_pool
        mock_pool.acquire.return_value = AsyncMock()

        conn = await db_pool.get_connection()

        mock_pool.acquire.assert_called_once()
        assert conn == mock_pool.acquire.return_value

    @pytest.mark.asyncio
    async def test_release_connection_with_pool(self, db_pool, mock_pool):
        """Test releasing connection with existing pool."""
        conn = AsyncMock()
        db_pool.pool = mock_pool

        await db_pool.release_connection(conn)

        mock_pool.release.assert_called_once_with(conn)

    @pytest.mark.asyncio
    async def test_release_connection_no_pool(self, db_pool):
        """Test releasing connection when no pool exists."""
        conn = AsyncMock()
        db_pool.pool = None

        await db_pool.release_connection(conn)

        # Should not raise error

    @pytest.mark.asyncio
    async def test_execute(self, db_pool, mock_pool):
        """Test execute method."""
        db_pool.pool = mock_pool
        mock_conn = AsyncMock()
        mock_conn.execute.return_value = "INSERT 1"
        mock_pool.acquire.return_value = mock_conn

        result = await db_pool.execute("INSERT INTO test VALUES ($1)", 123)

        mock_pool.acquire.assert_called_once()
        mock_conn.execute.assert_called_once_with("INSERT INTO test VALUES ($1)", 123)
        mock_pool.release.assert_called_once_with(mock_conn)
        assert result == "INSERT 1"

    @pytest.mark.asyncio
    async def test_fetch(self, db_pool, mock_pool):
        """Test fetch method."""
        db_pool.pool = mock_pool
        mock_conn = AsyncMock()
        mock_conn.fetch.return_value = [{"id": 1}]
        mock_pool.acquire.return_value = mock_conn

        result = await db_pool.fetch("SELECT * FROM test")

        mock_pool.acquire.assert_called_once()
        mock_conn.fetch.assert_called_once_with("SELECT * FROM test")
        mock_pool.release.assert_called_once_with(mock_conn)
        assert result == [{"id": 1}]

    @pytest.mark.asyncio
    async def test_fetchrow(self, db_pool, mock_pool):
        """Test fetchrow method."""
        db_pool.pool = mock_pool
        mock_conn = AsyncMock()
        mock_conn.fetchrow.return_value = {"id": 1}
        mock_pool.acquire.return_value = mock_conn

        result = await db_pool.fetchrow("SELECT * FROM test WHERE id = $1", 1)

        mock_pool.acquire.assert_called_once()
        mock_conn.fetchrow.assert_called_once_with("SELECT * FROM test WHERE id = $1", 1)
        mock_pool.release.assert_called_once_with(mock_conn)
        assert result == {"id": 1}

    @pytest.mark.asyncio
    async def test_fetchval(self, db_pool, mock_pool):
        """Test fetchval method."""
        db_pool.pool = mock_pool
        mock_conn = AsyncMock()
        mock_conn.fetchval.return_value = 42
        mock_pool.acquire.return_value = mock_conn

        result = await db_pool.fetchval("SELECT COUNT(*) FROM test")

        mock_pool.acquire.assert_called_once()
        mock_conn.fetchval.assert_called_once_with("SELECT COUNT(*) FROM test")
        mock_pool.release.assert_called_once_with(mock_conn)
        assert result == 42