from datetime import timedelta
from enum import IntEnum
from typing import Any, Dict, Optional

from jose import jwt

from ..settings import JWT_ALG, JWT_SECRET
from .token_exc import TokenDecodeError


class Token:
    """JWT Token class"""

    class TokenType(IntEnum):
        AUTH = 0

    def __init__(
        self,
        token_type: TokenType,
        data: Dict[str, Any],
        exp: Optional[timedelta] = None,
        token: Optional[str] = None,
    ):
        self.type = token_type
        self.data = data
        exp and self.data.update({"exp": exp})
        token and setattr(self, "token", token) or self._encode_token()

    def _encode_token(self):
        """Encode data to JWT token"""
        self.token = jwt.encode(
            {"t": self.type, **self.data}, JWT_SECRET, algorithm=JWT_ALG
        )

    # noinspection PyUnresolvedReferences
    @classmethod
    def decode_token(cls, token: str) -> Token:
        """Encoded token constructor"""
        try:
            t = jwt.decode(token, JWT_SECRET, algorithms=[JWT_SECRET])
        except jwt.JWTError:
            raise TokenDecodeError("Bad token")

        return cls(token_type=t.pop("t", -1), data=t, token=token)

    def __repr__(self):
        return self.token
