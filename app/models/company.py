from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CompanyCreate(BaseModel):
    name: str

class CompanyOut(BaseModel):
    id: UUID
    name: str
    created_at: Optional[datetime] = None


class CompanyMembership(BaseModel):
    user_id: UUID
    company_id: UUID
    role: str