from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from .__main__ import engine

# noinspection PyTypeChecker
async_session: AsyncSession = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


def session(func):
    """Database provider for controllers
    Update func kwarg "db" as Async Session"""

    async def wrap(*args, **kwargs):
        async with async_session() as db:
            async with db.begin():
                kwargs.get("db") or kwargs.update({"db": db})
                return func(*args, **kwargs)

    return wrap
