from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    email: str
    password: str
    role: Optional[str] = None

class UserOut(BaseModel):
    id: UUID
    email: str
    role: str
    created_at: datetime

class UserLogin(BaseModel):
    email: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
