from pydantic import BaseModel


class EmailExists(BaseModel):
    exists: bool = False
