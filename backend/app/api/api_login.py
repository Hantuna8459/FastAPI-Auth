from datetime import timedelta, datetime
from typing import Any
from ..api.dependencies import CurrentUser

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.core.security import (
    create_access_token,
    create_refresh_token,
)
from ..core.config import settings
from ..api.dependencies import SessionDep
from ..models.token import Token
from ..models.user import LoginRequest
from ..crud import authenticate

router = APIRouter()

@router.post("/login", response_model=Token)
def login_with_token(session: SessionDep,
                     form_data: OAuth2PasswordRequestForm = Depends())\
                    ->Token:
    user = authenticate(
        session=session,
        credential=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(status_code=400, detail="incorrect email or password")
    if not user.is_root.is_active:
        raise HTMLResponse(status_code=400, detail="inactive user")
    user.is_root.last_login = datetime.now()
    session.commit()
    session.refresh(user)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token=create_access_token(
        user.id, 
        expires_delta=access_token_expires,
    )
    
    # Create refresh token
    refresh_token=create_refresh_token(
        expires_delta=refresh_token_expires,
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    
@router.post("/login/test-token")
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
