from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.core import security
from backend.app.core.config import settings
from backend.app.api.dependencies import SessionDep
from backend.app.models.user import Token
from backend.app import crud

router = APIRouter()

@router.post("/login")
def login_with_token(response:Response, session:SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()])->Token:
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="incorrect email or password")
    if not user.is_active:
        raise HTMLResponse(status_code=400, detail="inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    # Store token in httponly cookie 
    response.set_cookie(key="access_token", 
                        value=f"bearer{access_token}",
                        httponly=True, 
                        secure=True,
                        )
    
    access_token=security.create_access_token(
        user.user_id, 
        expires_delta=access_token_expires,
    )
    
    # Create refresh token
    refresh_token=security.create_refresh_token(
        user.user_id, 
        expires_delta=refresh_token_expires,
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )