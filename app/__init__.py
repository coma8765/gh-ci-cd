import os

from fastapi import FastAPI
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine

app = FastAPI()

engine: Engine = create_async_engine(
    os.getenv("DB_URI") or "sqlite+aiosqlite://", echo=True
)
