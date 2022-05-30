import datetime
from typing import Concatenate, Literal

from passlib.handlers.bcrypt import bcrypt
from pydantic import BaseModel, EmailStr, SecretStr, constr


class BaseUser(BaseModel):
    email: EmailStr


class RefUser(BaseUser):
    password: SecretStr

    def get_hash_password(self) -> str:
        return bcrypt.hash(self.password.get_secret_value())

    @staticmethod
    def validate_hash_password(bare_password: SecretStr, hashed_password: str):
        return bcrypt.verify(bare_password.get_secret_value(), hashed_password)


class User(BaseUser):
    id: int
    email_confirm: bool = False
    create_date: datetime.datetime


class Token(BaseModel):
    type: Literal['bearer'] = "bearer"
    token: constr(max_length=500)
