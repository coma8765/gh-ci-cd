import os
from typing import Optional

import asyncpg

pool: Optional[asyncpg.Pool] = None
Session = asyncpg.Connection
nested_session: Optional[Session] = None


def set_nested_connection(conn):
    global nested_session

    nested_session = conn


async def startup(loop=None):
    global pool

    pool = await asyncpg.create_pool(
        f"postgresql://"
        f"{os.getenv('POSTGRES_USER', None) or 'postgres'}:"
        f"{os.getenv('POSTGRES_PASSWORD', None) or 'password'}@"
        f"{os.getenv('POSTGRES_HOST', None) or 'localhost'}:"
        f"{os.getenv('POSTGRES_PORT', None) or 5432}/"
        f"{os.getenv('POSTGRES_DATABASE', None) or 'postgres'}",
        loop=loop
    )
