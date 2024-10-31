import time
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text, update, delete, create_engine, select, insert, Float, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.future import select
from sqlalchemy import MetaData, Column, Integer, String
import sqlalchemy as db
from typing import Optional
import asyncio

DATABASE_URL = "postgresql://user:password@localhost/BTC_ETH"
engine = db.create_engine(DATABASE_URL)
connection = engine.connect()
metadata = db.MetaData()
"""

price = db.Table('price', metadata,
                 db.Column('id', db.Integer, primary_key=True),
                 db.Column('ticker', db.String),
                 db.Column('pricee', db.Float),
                 db.Column('timestamp', db.Integer)
                 )"""
price_table = db.Table('price', metadata, autoload_with=engine)
select_price = price_table.select()
selectt = connection.execute(select_price)

print(selectt.fetchall())

"""

"""
"""
Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)




async def get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def main():
    async with async_session() as session:
        async with session.begin():
            user = await get_user_by_id(session, 1)
            print(user)

import asyncio
asyncio.run(main())    """
