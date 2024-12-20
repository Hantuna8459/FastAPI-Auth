from jose import jwt
from jwt.exceptions import InvalidTokenError

from typing import Annotated

from pydantic import ValidationError
from sqlmodel import Session

from ..models.user import User
from ..models.token import TokenPayload

from ..core.config import settings
from ..core.db_connect import get_db

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
        
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="login")

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep)->User:
    try:
        payload = jwt.decode(
            token, settings.public_key, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_root.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_root.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
        