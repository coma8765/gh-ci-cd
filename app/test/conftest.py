import asyncio

import pytest
from asyncpg.transaction import Transaction
from pydantic.config import BaseConfig

from app import db


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(autouse=True, scope="session")
async def session(event_loop):
    await db.startup(loop=event_loop)

    async with db.pool.acquire() as conn:
        conn: db.Session
        tr: Transaction = conn.transaction()

        await tr.start()
        db.set_nested_connection(conn)

        yield

        await tr.rollback()


BaseConfig.orm_mode = True
