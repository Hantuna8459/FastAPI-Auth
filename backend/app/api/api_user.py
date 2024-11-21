from typing import Any

from fastapi import APIRouter, HTTPException

from ..models.user import User
from ..api.dependencies import CurrentUser, SessionDep, TokenDep

router = APIRouter()



    