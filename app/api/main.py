from fastapi import APIRouter

from app.api.routes import devices, login, sensors, users, utils

api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(devices.router)
api_router.include_router(sensors.router)
