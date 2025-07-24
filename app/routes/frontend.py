# app/routes/frontend.py
from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()

@router.get("/login")
def login(): return FileResponse("static/login.html")

@router.get("/register")
def register(): return FileResponse("static/register.html")

@router.get("/dashboard")
def dashboard(): return FileResponse("static/dashboard.html")
