from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserCreate, UserOut, UserLogin, TokenOut
from app.utils.security import verify_password, create_access_token
from app.crud import user as crud
from app.db import get_db
from datetime import timedelta
from app.models.user import UserOut
from app.utils.security import get_current_user
import asyncpg
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=201)
async def create_user(user: UserCreate, conn: asyncpg.Connection = Depends(get_db)):
    return await crud.create_user(conn, user)

@router.get("/me")
async def get_logged_in_user(user: dict = Depends(get_current_user)):
    return {
        "id": user["id"],
        "email": user["email"],
        "role": user.get("role", "user")
    }

@router.get("/email/{email}", response_model=UserOut)
async def get_user(email: str, conn: asyncpg.Connection = Depends(get_db)):
    user = await crud.get_user_by_email(conn, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/login", response_model=TokenOut)
async def login(user: UserLogin, conn: asyncpg.Connection = Depends(get_db)):
    db_user = await crud.get_user_by_email(conn, user.email)

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"sub": str(db_user["id"]), "role": db_user["role"]},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID, conn: asyncpg.Connection = Depends(get_db)):
    user = await crud.get_user_by_id(conn, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user