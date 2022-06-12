from typing import List

from .schema import *
from ..auth import UserShort
from ...dependencies import Session, session


@session
async def user_list(params: UserListSearch, db: Session) -> List[UserShort]:
    """List users with params"""
    sql = "SELECT id, email FROM users"

    if any(params.dict().values()):
        sql += " FROM"
        sql += " and".join(
            [
                params.email and f" email='{params.email}'",
                params.full_name
                and f" lower(full_name)" f" LIKE 'f{params.full_name}'",
                params.telephone and f" telephone='{params.telephone}'",
            ]
        )

    print(sql)

    return list(map(UserShort.from_orm, await db.fetch(sql)))
