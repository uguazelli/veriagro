from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from app.models.company import CompanyCreate, CompanyOut, CompanyMembership
from app.crud import company as crud_company
import asyncpg

router = APIRouter()

@router.post("/", status_code=201)
async def create_company( company: CompanyCreate, db=Depends(get_db)):
    """
    Create a new company.
    """
    try:
        new_company = await crud_company.create_company(db, company)
        return new_company
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Company with this name already exists")



@router.get("/{company_id}", response_model=CompanyOut)
async def get_company(company_id: int, db=Depends(get_db)):
    """
    Get a company by ID.
    """
    company = await crud_company.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.delete("/{company_id}", status_code=204)
async def delete_company( company_id: int, db=Depends(get_db)):
    """
    Delete a company by ID.
    """
    deleted = await crud_company.delete_company(db, company_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"detail": "Company deleted successfully"}


@router.post("/membership", status_code=201)
async def create_membership(membership: CompanyMembership, db=Depends(get_db)):
    """
    Create a membership for a user in a company.
    """
    try:
        new_membership = await crud_company.create_membership(db, membership)
        return new_membership
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Membership already exists")


@router.get("/membership/{user_id}", response_model=list[CompanyOut])
async def get_user_companies(user_id: str, db=Depends(get_db)):
    """
    Get all companies a user is a member of.
    """
    companies = await crud_company.get_user_companies(db, user_id)
    if not companies:
        raise HTTPException(status_code=404, detail="No companies found for this user")
    return companies

@router.delete("/membership/{user_id}/{company_id}", status_code=204)
async def delete_membership(user_id: str, company_id: str, db=Depends(get_db)):
    """
    Delete a user's membership in a company.
    """
    deleted = await crud_company.delete_membership(db, user_id, company_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Membership not found")
    return {"detail": "Membership deleted successfully"}

