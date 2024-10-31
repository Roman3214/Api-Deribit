import aiohttp
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import  insert
import asyncio



async def fetch_price(session, url):
    async with session.get(url) as response:
        return await response.json()
    

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/BTC_ETH"

class Base (AsyncAttrs, DeclarativeBase):
    pass

class quotes(Base):
    __tablename__ = "price"
    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] 
    pricee: Mapped[float] 
    timestamp: Mapped[float]


async def insert_price(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session() as session_db:
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session_aiohttp:
            while True:
                btc_price = await fetch_price(session_aiohttp, 'https://www.deribit.com/api/v2/public/get_index_price?index_name=btc_usd')
                eth_price = await fetch_price(session_aiohttp, 'https://www.deribit.com/api/v2/public/get_index_price?index_name=eth_usd')
                
                insert_data_btc = insert(quotes).values({
                    'ticker': "BTC-USD",
                    'pricee': btc_price["result"]['index_price'],
                    'timestamp': btc_price['usIn'] / 1000000
                })

                insert_data_eth = insert(quotes).values({
                    'ticker': "ETH-USD",
                    'pricee': eth_price["result"]['index_price'],
                    'timestamp': eth_price['usIn'] / 1000000
                })

                async with session_db.begin():
                    await session_db.execute(insert_data_btc)
                    await session_db.execute(insert_data_eth)
                    await session_db.commit()

                print("Inserted BTC price:", btc_price["result"]['index_price'])
                print("Inserted ETH price:", eth_price["result"]['index_price'])
                
                await asyncio.sleep(5)



async def async_main() -> None:
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


    await insert_price(async_session)
    await engine.dispose()

    
asyncio.run(async_main())