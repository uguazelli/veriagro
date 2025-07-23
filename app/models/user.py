from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: Optional[str]
    senha: str

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str]
    criado_em: datetime
