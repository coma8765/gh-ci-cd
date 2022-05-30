import pytest
from asyncpg.transaction import Transaction

from app import db


@pytest.fixture()
async def session():
    await db.startup()
    async with db.pool.acquire() as conn:
        conn: db.Session

        tr: Transaction = conn.transaction()
        await tr.start()

        db.set_nested_connection(conn)

        yield

        await tr.rollback()
