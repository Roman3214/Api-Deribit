import pytest
import aiohttp
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from client import fetch_price, insert_price, Base, quotes

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/test_db"

@pytest.fixture
async def async_engine():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def async_session(async_engine):
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
    yield async_session

@pytest.mark.asyncio
async def test_fetch_price():
    async with aiohttp.ClientSession() as session:
        btc_price = await fetch_price(session, 'https://www.deribit.com/api/v2/public/get_index_price?index_name=btc_usd')
        assert 'result' in btc_price
        assert 'index_price' in btc_price['result']

@pytest.mark.asyncio
async def test_insert_price(async_session):
    async with async_session() as session_db:
        await insert_price(async_session)
        async with session_db() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM price"))
            count = result.scalar()
            assert count > 0



"""import pytest
from httpx import AsyncClient
from api import app

@pytest.mark.asyncio
async def test_get_prices():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/price/?ticker=btc_usd")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_latest_price():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/price/latest/?ticker=btc_usd")
        if response.status_code == 200:
            assert isinstance(response.json(), dict)
        else:
            assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_price_by_date():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/price/filter/?ticker=btc_usd&start_date=1609459200&end_date=1612137600")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
"""