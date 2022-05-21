from starlette.testclient import TestClient


def test_available(client: TestClient):
    r = client.get("/")

    assert r.status_code == 200
    assert {"status": "success"} == r.json()
