import pytest
from asyncpg.transaction import Transaction
from httpx import AsyncClient

from ... import app, db


@pytest.fixture()
async def client() -> AsyncClient:
    await db.startup()

    async with db.pool.acquire() as conn:
        conn: db.Session
        tr: Transaction = conn.transaction()

        await tr.start()
        db.set_nested_connection(conn)

        yield AsyncClient(app=app, base_url="http://test")
