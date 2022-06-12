import random

import pytest

from ...controllers.auth import *


@pytest.fixture()
def create_user():
    async def inner(user_ref: Optional[UserRef] = None, db=None):
        if user_ref is None:
            user_ref = UserRef(
                email=f"user-test-" f"{random.randint(10000000, 99999999)}@test.mail",
                password="some_password",
            )

        return await signup(user_ref, db=db)

    return inner
