import random
from typing import Callable, Awaitable, Optional

import pytest

from ...controllers.auth import *


@pytest.fixture()
def create_user(session):
    async def inner(user_ref: Optional[RefUser] = None, db=None):
        if user_ref is None:
            user_ref = RefUser(
                email=f"user-test-"
                      f"{random.randint(10000000, 99999999)}@test.mail",
                password="some_password"
            )

        return await signup(user_ref, db=db)

    return inner
