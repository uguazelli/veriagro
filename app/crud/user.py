# app/crud/user.py
from app.models.user import UserCreate, UserOut, UserInDB
from app.utils.security import hash_password
import asyncpg
import uuid

async def create_user(conn: asyncpg.Connection, user: UserCreate) -> UserOut:
    hashed_password = hash_password(user.password)  # <- Corrigido
    user_id = uuid.uuid4()
    query = """
        INSERT INTO users (id, email, password, created_at)
        VALUES ($1, $2, $3, now())
        RETURNING id, email, created_at
    """
    row = await conn.fetchrow(query, user_id, user.email, hashed_password)
    return UserOut(id=row['id'], email=row['email'], created_at=row['created_at'])


async def get_user_by_email(conn: asyncpg.Connection, email: str) -> UserInDB:
    query = "SELECT id, email, created_at, password FROM users WHERE email = $1"
    row = await conn.fetchrow(query, email)
    if row:
        return UserInDB(
            id=row['id'],
            email=row['email'],
            created_at=row['created_at'],
            hashed_password=row['password']
        )
    return None


async def get_user_by_id(conn: asyncpg.Connection, user_id: uuid.UUID) -> UserOut:
    query = "SELECT id, email, created_at FROM users WHERE id = $1"
    row = await conn.fetchrow(query, user_id)
    if row:
        return UserOut(id=row['id'], email=row['email'], created_at=row['created_at'])
    return None

