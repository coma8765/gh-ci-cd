from datetime import timedelta
from enum import IntEnum
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .token_controller import Token
from .auth_exc import AuthError
from ..dependencies import session
from ..models import SignInRef, User, UserBase


@session
async def auth(token: Token, db: Optional[AsyncSession]) -> User:
    """User auth controller
    :param token: Token
    :param db: optional, default get with wrapper
    :return User model
    :raises AuthError - Token has incorrect type or user for token not found"""

    if token.type != Token.TokenType.AUTH or not token.data.get("v"):
        raise AuthError("Token type incorrect")

    user = (
        await db.execute(select(User).where(User.id == token.data["v"]))
    ).scalar_one_or_none()

    if not user:
        raise AuthError("User not found")

    return user


@session
async def signin(signin_ref: SignInRef, db: Optional[AsyncSession]) -> Optional[User]:
    """"""
    pass


@session
async def signup(user_data: UserBase, db: Optional[AsyncSession]) -> Optional[User]:
    """"""
    pass


def create_auth_token(user: User) -> Token:
    """Helper for create auth token"""
    return Token(
        token_type=Token.TokenType.AUTH, data={"v": user.id}, exp=timedelta(days=90)
    )
