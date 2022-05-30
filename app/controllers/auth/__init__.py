import os
from typing import Optional

from jose import jwt

from .exc import *
from .schema import *
from ...dependencies import Session, session


@session
async def signup(base_user: RefUser, db: Optional[Session]) -> User:
    """SignUp user controller"""
    if await check_email_exists(base_user.email, db=db):
        raise UserAlreadyExists("User already exists")

    user_id = await db.fetchval(
        "insert into users (email, hashed_password) "
        "VALUES ($1, $2) RETURNING id",
        base_user.email, base_user.get_hash_password()
    )

    return User(
        id=user_id,
        email=base_user.email,
        create_date=datetime.datetime.now()
    )


@session
async def signin(base_user: RefUser, db: Optional[Session]) -> User:
    """Login user by email and bare password"""
    user = await db.fetchrow(
        "SELECT id, email, hashed_password, create_date "
        "FROM users WHERE email = $1",
        base_user.email
    )

    if not user or not RefUser.validate_hash_password(
            base_user.password, user["hashed_password"]
    ):
        raise SignInWrong("Incorrect username or password")

    return User(**user)


@session
async def check_email_exists(
        email: EmailStr,
        db: Optional[Session]
) -> bool:
    """Check email exists in application"""
    return bool(
        await db.fetchrow("SELECT id FROM users WHERE email = $1", email)
    )


@session
async def get_user_by_token(token: Token, db: Optional[Session]) -> User:
    user_id = get_user_id_by_token(token)
    return User(**await db.fetchrow(
        "SELECT id, email, hashed_password, create_date "
        "FROM users WHERE id = $1",
        user_id
    ))


def create_auth_token(user_id: int) -> Token:
    """Getting JWT token by user id"""
    return Token(
        token=jwt.encode(
            {
                "exp": datetime.datetime.now() + datetime.timedelta(days=90),
                "u": f"a{user_id}"
            },
            os.getenv("JWT_SECRET", None) or "asdamdlmwdmwom",
            algorithm="HS256"
        ),
        type="bearer"
    )


def get_user_id_by_token(token: Token) -> int:
    """Get auth user id by token"""
    try:
        d: str = jwt.decode(
            token.token,
            os.getenv("JWT_SECRET", None) or "asdamdlmwdmwom",
            algorithms=["HS256"]
        ).get("u", None)
    except jwt.JWTError:
        raise BadToken

    if not d or not d.startswith("a"):
        raise BadToken

    return int(d[1:])
