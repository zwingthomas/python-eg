import pytest
from httpx import AsyncClient
from main import app

# TODO: Mock this


@pytest.mark.asyncio
async def test_create_and_read_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/items", json={"text": "buy milk"})
        assert r.status_code == 201
        data = r.json()
        r2 = await ac.get(f"/items/{0}")
        assert r2.json() == data
