import os
import asyncpg
from dotenv import load_dotenv
from typing import AsyncGenerator

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Pool global
db_pool: asyncpg.Pool = None

async def init_db_pool():
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    print("✅ Pool de conexões PostgreSQL criado.")

async def close_db_pool():
    global db_pool
    await db_pool.close()
    print("🛑 Pool de conexões PostgreSQL encerrado.")

# Generator compatível com FastAPI Depends
async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    async with db_pool.acquire() as conn:
        yield conn
