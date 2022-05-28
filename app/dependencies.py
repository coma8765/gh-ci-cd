import functools
from functools import wraps
from typing import (
    Any,
    Awaitable,
    Callable,
    Concatenate,
    NewType,
    Optional,
    ParamSpec,
    TypeVar,
    cast,
    ParamSpecKwargs,
    ParamSpecArgs,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from . import engine

# noinspection PyTypeChecker
async_session: AsyncSession = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# TCallable = TypeVar("TCallable", bound=Callable)
# PS = ParamSpec("P")
# PSA = ParamSpecArgs(PS)
# PSK = ParamSpecKwargs(PS)

PS = ParamSpec("PS", bound=Concatenate[ParamSpec("PS"), AsyncSession])
DB = NewType("db", AsyncSession)


def session(func: Callable[[Concatenate[DB, PS]], ...]) -> Callable[PS, ...]:
    """Database provider for controllers
    Update func kwarg "db" as Async Session"""

    @functools.wraps(func, updated=["db"])
    async def wrap(
        *args, db: Optional[AsyncSession] = None, **kwargs
    ) -> Callable[PS, ...]:
        async with async_session() as db_:
            async with db.begin():
                kwargs.update({"db": db or db_})
                return func(*args, **kwargs)

    return wrap
