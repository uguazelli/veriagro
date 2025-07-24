from fastapi import APIRouter, Depends
from app.utils.security import get_current_admin

router = APIRouter()

# Only JWTs with role = admin can access /admin/dashboard.
@router.get("/dashboard")
async def admin_dashboard(admin_user=Depends(get_current_admin)):
    return {"message": f"Welcome admin {admin_user['username']}"}
