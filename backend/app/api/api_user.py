from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.api.dependencies import CurrentUser, SessionDep, TokenDep
from app.models.user import Token
from app import crud

router = APIRouter()
    