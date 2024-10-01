from fastapi import APIRouter

from backend.app.api import api_login,api_logout

api_router=APIRouter()
api_router.include_router(api_login.router)