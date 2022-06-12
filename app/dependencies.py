import functools
from typing import Awaitable, Callable, Concatenate, NewType, Optional, ParamSpec

from .db import Session

PS = ParamSpec("PS", bound=Concatenate[Session, ParamSpec("PS")])
DB = NewType("db", Session)
RT = ParamSpec("RT")


def session(
    func: Callable[Concatenate[DB, PS], Awaitable[RT]]
) -> Callable[PS, Awaitable[RT]]:
    @functools.wraps(func)
    async def wrapper(*args, db: Optional[Session] = None, **kwargs):
        from .db import nested_session

        if db:
            return await func(*args, db=db, **kwargs)

        if nested_session:
            return await func(*args, db=nested_session, **kwargs)

        from .db import pool

        if pool is None:
            from importlib import reload
            from . import db as db_

            await db_.startup()
            reload(db_)

        async with pool.acquire() as conn:
            conn: Session

            async with conn.transaction():
                return await func(*args, db=conn, **kwargs)

    return wrapper


__all__ = ["session", "Session"]
