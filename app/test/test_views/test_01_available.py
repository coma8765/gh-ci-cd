from httpx import AsyncClient


async def test_available(client: AsyncClient):
    r = await client.get("/")

    assert r.status_code == 200
    assert {"status": "success"} == r.json()
