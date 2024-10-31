
Api-Deribit - это приложение на FastAPI для получения и хранения цен на криптовалюты с биржи Deribit.

Оглавление

Описание

Требования

Установка

Использование

Тестирование


Описание

Api-Deribit позволяет получать текущие цены на криптовалюты BTC и ETH с биржи Deribit и сохранять их в базе данных PostgreSQL. Приложение предоставляет несколько эндпоинтов для получения цен и фильтрации данных по дате.


Требования

Python 3.9+

PostgreSQL

FastAPI

SQLAlchemy

aiohttp

Установка


Клонируйте репозиторий:
git clone https://github.com/yourusername/api-deribit.git

cd api-deribit


Установите зависимости:

python -m venv venv

source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`

pip install -r requirements.txt


Настройте базу данных PostgreSQL:
psql -U user -d BTC_ETH -c "CREATE DATABASE BTC_ETH;"


Запустите приложение:
uvicorn main:app --host localhost --port 8000 --reload


Использование


Эндпоинты
GET /price/: Получить все цены для указанного тикера.
curl -X 'GET' \
  'http://localhost:8000/price/?ticker=btc_usd' \
  -H 'accept: application/json'
  

GET /price/latest/: Получить последнюю цену для указанного тикера.
curl -X 'GET' \
  'http://localhost:8000/price/latest/?ticker=btc_usd' \
  -H 'accept: application/json'
  

GET /price/filter/: Получить цены для указанного тикера в заданном диапазоне дат.
curl -X 'GET' \
  'http://localhost:8000/price/filter/?ticker=btc_usd&start_date=1609459200&end_date=1612137600' \
  -H 'accept: application/json'


Тестирование

Для запуска тестов используйте pytest:

Установите зависимости для тестирования:

pip install pytest pytest-asyncio aiohttp


Запустите тесты:

pytest
