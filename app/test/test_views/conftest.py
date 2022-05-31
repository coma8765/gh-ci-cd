import pytest
from httpx import AsyncClient

from ... import app


@pytest.fixture()
async def client() -> AsyncClient:
    yield AsyncClient(app=app, base_url="http://test")
