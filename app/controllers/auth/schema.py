import datetime
from typing import Concatenate, Literal

from passlib.handlers.bcrypt import bcrypt
from pydantic import BaseModel, EmailStr, SecretStr, constr

BaseStr = constr(max_length=60)
TelephoneStr = constr(max_length=12, regex=r"\+7\d{10}")


class BaseUser(BaseModel):
    email: EmailStr


class UserRef(BaseUser):
    password: SecretStr

    def get_hash_password(self) -> str:
        return bcrypt.hash(self.password.get_secret_value())

    @staticmethod
    def validate_hash_password(bare_password: SecretStr, hashed_password: str):
        return bcrypt.verify(bare_password.get_secret_value(), hashed_password)


class UserShort(BaseUser):
    id: int


class User(UserShort):
    email_confirm: bool = False
    create_date: datetime.datetime
    full_name: BaseStr | None
    icon_id: constr(max_length=20) | None
    telephone: TelephoneStr | None
    country: BaseStr | None
    city: BaseStr | None


class Token(BaseModel):
    type: Literal['bearer'] = "bearer"
    token: constr(max_length=500)
