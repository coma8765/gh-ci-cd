from .fixture_auth import *


@pytest.mark.asyncio
async def test_signup_base(create_user):
    d = UserRef(
        email=f"user-test-{random.randint(10000000, 99999999)}@t.com",
        password="password",
    )
    u = await create_user(d)

    assert u.email == d.email
    assert isinstance(u.id, int)


async def test_signup_duplicate(create_user):
    d = UserRef(
        email=f"user-test-{random.randint(10000000, 99999999)}@t.com",
        password="password",
    )
    await create_user(d)

    with pytest.raises(UserAlreadyExists):
        await create_user(d)


async def test_signin(create_user):
    r = UserRef(
        email=f"user-test-{random.randint(10000000, 99999999)}@t.com",
        password="password",
    )

    u_o = await create_user(r)
    u_l = await signin(r)

    assert u_o.dict() == u_l.dict()


def test_token_generation(create_user):
    assert 1 == get_user_id_by_token(create_auth_token(1))
    assert 1 != get_user_id_by_token(create_auth_token(2))


async def test_auth_by_token(create_user):
    u_o = await create_user(None)
    u_l = await get_user_by_token(create_auth_token(u_o.id))
    assert u_o.dict() == u_l.dict()


async def test_auth_by_token_error():
    with pytest.raises(BadToken):
        get_user_id_by_token(Token(token="some-wrong-token", type="bearer"))
