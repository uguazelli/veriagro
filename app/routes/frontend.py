# app/routes/frontend.py
from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()

@router.get("/login")
def login(): return FileResponse("static/login/index.html")

@router.get("/register")
def register(): return FileResponse("static/register.html")

@router.get("/")
def dashboard(): return FileResponse("static/dashboard/index.html")

@router.get("/device-settings")
def dashboard(): return FileResponse("static/device_settings/index.html")

@router.get("/sensor-settings/{id}")
def dashboard(): return FileResponse("static/device_settings/sensor.html")

@router.get("/topics-settings/{id}")
def dashboard(): return FileResponse("static/device_settings/topics.html")