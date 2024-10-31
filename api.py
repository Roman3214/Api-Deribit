from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import asyncpg

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняемый при старте приложения
    app.state.pool = await asyncpg.create_pool("postgresql://user:password@localhost/BTC_ETH")
    yield
    # Код, выполняемый при завершении работы приложения
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/price/")
async def get_prices(ticker: str):
    async with app.state.pool.acquire() as connection:
        rows = await connection.fetch("SELECT * FROM price WHERE ticker = $1", ticker)
        return [dict(row) for row in rows]

@app.get("/price/latest/")
async def get_latest_price(ticker: str):
    async with app.state.pool.acquire() as connection:
        row = await connection.fetchrow("SELECT * FROM price WHERE ticker = $1 ORDER BY timestamp DESC LIMIT 1", ticker)
        if row:
            return dict(row)
        raise HTTPException(status_code=404, detail="Price not found")

@app.get("/price/filter/")
async def get_price_by_date(ticker: str, start_date: float, end_date: float):
    async with app.state.pool.acquire() as connection:
        rows = await connection.fetch(
            "SELECT * FROM price WHERE ticker = $1 AND timestamp BETWEEN $2 AND $3",
            ticker, start_date, end_date
        )
        return [dict(row) for row in rows]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="localhost", port=8000, reload=True)
