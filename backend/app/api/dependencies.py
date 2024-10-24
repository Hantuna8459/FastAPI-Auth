from jose import jwt
from jwt.exceptions import InvalidTokenError

from collections.abc import Generator
from typing import Annotated

from pydantic import ValidationError
from sqlmodel import Session

from ..core.database import engine
from ..models.user import User
from ..models.token import TokenPayload

from ..core.config import settings
from ..core import security

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]

def get_current_user(session: SessionDep, token: TokenDep)->User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
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
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
        