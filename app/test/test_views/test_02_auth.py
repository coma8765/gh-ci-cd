import random
from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient
from starlette import status

from ...controllers import auth as c


@pytest.fixture()
def user(client: AsyncClient):
    async def inner(ref: Optional[c.UserRef] = None):
        if ref is None:
            r = random.randint(10000000, 99999999)
            ref = c.UserRef(email=f"test-{r}@mail.com", password="password")

        j = await client.post(
            "/signup", json={**ref.dict(), "password": ref.password.get_secret_value()}
        )

        assert j.status_code == status.HTTP_201_CREATED

        return {**j.json(), "password": ref.password.get_secret_value()}

    return inner


async def test_signup(client):
    r = random.randint(10000000, 99999999)
    ref = c.UserRef(email=f"test-{r}@mail.com", password="password")

    j = await client.post(
        "/signup", json={**ref.dict(), "password": ref.password.get_secret_value()}
    )

    assert j.status_code == status.HTTP_201_CREATED

    data: Dict[str, Any] = j.json()

    assert isinstance(data["id"], int)
    assert data["email"] == ref.email


async def test_signup_duplicate(client):
    r = random.randint(10000000, 99999999)
    ref = c.UserRef(email=f"test-{r}@mail.com", password="password")

    r = await client.post(
        "/signup", json={**ref.dict(), "password": ref.password.get_secret_value()}
    )

    assert r.status_code == status.HTTP_201_CREATED

    e = await client.post(
        "/signup", json={**ref.dict(), "password": ref.password.get_secret_value()}
    )

    assert e.status_code == status.HTTP_400_BAD_REQUEST
    assert e.json() == {"detail": "UserShort already exists"}


async def test_signin(user, client):
    d = await user()
    r = await client.post(
        "/signin", json={"email": d["email"], "password": d["password"]}
    )

    assert r.status_code == status.HTTP_200_OK

    data = r.json()

    assert data["type"] == "bearer"
    assert isinstance(data["token"], str)


async def test_signin_incorrect(client):
    r = await client.post(
        "/signin", json={"email": "some@mail.com", "password": "random-pass"}
    )

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.json() == {"detail": "Incorrect username or password"}


async def test_check_email_exists(user, client):
    u = await user()
    r = await client.get(f"/check_email_exists?email={u['email']}")

    assert r.status_code == status.HTTP_200_OK
    assert r.json() == {"exists": True}


async def test_check_email_not_exists(client):
    r = await client.get(f"/check_email_exists?email=aa@mail.com")

    assert r.status_code == status.HTTP_200_OK
    assert r.json() == {"exists": False}
