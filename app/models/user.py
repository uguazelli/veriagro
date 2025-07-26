from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    created_at: Optional[datetime] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserOut):
    hashed_password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"