from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class SignInRef(BaseModel):
    email: str
    password: str


class UserBase:
    email = Column(String(100), unique=True, nullable=False)


class User(UserBase, Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email_confirm = Column(Boolean, default=False)
    hashed_password = Column(String(100))  # TODO: Set exact string length
    # TODO: Add other columns
