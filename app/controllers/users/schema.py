from pydantic import BaseModel, EmailStr

from ..auth import BaseStr, TelephoneStr


class UserListSearch(BaseModel):
    email: EmailStr | None
    full_name: BaseStr | None
    telephone: TelephoneStr | None

    page: int | None
