from fastapi import APIRouter

from backend.app.api import api_login,api_user

api_router=APIRouter()
api_router.include_router(api_login.router, tags=["auth"])
api_router.include_router(api_user.router, tags=["user"])