from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserCreate, UserOut
from app.crud import user as crud
from app.db import get_db
from typing import List
import asyncpg

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=201)
async def create_user(user: UserCreate, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.create_user(conn, user)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, conn: asyncpg.Connection = Depends(get_db)):
    user = await crud.get_user_by_id(conn, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
