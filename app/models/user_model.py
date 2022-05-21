from sqlalchemy import Boolean, Column, Integer, String

from .base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    email_confirm = Column(Boolean, default=False)
    hashed_password = Column(String(100))  # TODO: Set exact string length
    # TODO: Add other columns
