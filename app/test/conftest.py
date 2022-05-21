import pytest
from starlette.testclient import TestClient

from ..__main__ import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
