from sqlmodel import SQLModel, Field
from typing import Optional

class Price(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str
    price: float
    timestamp: int
