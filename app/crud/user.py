from app.models.user import UserCreate
import asyncpg

async def create_user(conn: asyncpg.Connection, user: UserCreate):
    row = await conn.fetchrow(
        """
        INSERT INTO users (username, email, senha)
        VALUES ($1, $2, $3)
        RETURNING id, username, email, criado_em
        """,
        user.username, user.email, user.senha
    )
    return dict(row)

async def get_user_by_id(conn: asyncpg.Connection, user_id: int):
    row = await conn.fetchrow(
        "SELECT id, username, email, criado_em FROM users WHERE id = $1", user_id
    )
    return dict(row) if row else None
