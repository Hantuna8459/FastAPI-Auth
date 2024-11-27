import os

from datetime import timezone, timedelta, datetime
from typing import Any

import scrypt
from jose import jwt
from passlib.context import CryptContext

from backend.app.core.config import settings

pwd_context = CryptContext(schemes=["scrypt"], deprecated="auto")

def create_access_token(subject: str | Any, expires_delta: timedelta)->str:
    expire = datetime.now(timezone.utc)+expires_delta
    to_encode = {
        "exp":expire, 
        "sub":str(subject),
    }
    encoded_access = jwt.encode(to_encode, settings.private_key, algorithm=settings.ALGORITHM)
    return encoded_access

def create_refresh_token(expires_delta: timedelta)->str:
    expire = datetime.now(timezone.utc)+expires_delta
    to_encode = {
        "exp":expire,
        # need something here
        "type":"refresh",
    }
    encoded_refresh = jwt.encode(to_encode, settings.PRIVATE_KEY, algorithm=settings.ALGORITHM)
    return encoded_refresh

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str, maxtime=0.5) -> bool:
    try:
        scrypt.encrypt(plain_password, hashed_password, maxtime)
        return True
    except scrypt.error:
        return False
