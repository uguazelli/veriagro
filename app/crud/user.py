# app/crud/user.py
from app.models.user import UserCreate
from app.utils.security import hash_password
import asyncpg
import uuid

async def create_user(conn: asyncpg.Connection, user: UserCreate):
    id = str(uuid.uuid4())
    hashed_password = hash_password(user.password)
    user_role = user.role or "admin"

    row = await conn.fetchrow(
        """
        INSERT INTO users ( id, email, password, role)
        VALUES ($1, $2, $3, $4)
        RETURNING id, email, role, created_at
        """,
        id, user.email, hashed_password, user_role
    )
    return dict(row)

async def get_user_by_id(conn: asyncpg.Connection, user_id: uuid):
    row = await conn.fetchrow(
        """
        SELECT id, email, role, created_at FROM users
        WHERE id = $1
        """,
        user_id
    )
    return dict(row) if row else None

async def get_user_by_email(conn: asyncpg.Connection, email: str):
    row = await conn.fetchrow(
        "SELECT id, email, password, role, created_at FROM users WHERE email = $1",
        email
    )
    return dict(row) if row else None
