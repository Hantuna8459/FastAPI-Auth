from typing import Any

from fastapi import APIRouter, HTTPException

from ..models.user import (
    User,
    UserCreate,
    UserRegister,
)
from ..crud import (
    get_user_by_username_or_email,
    create_user,
)
from ..api.dependencies import SessionDep

router = APIRouter()

@router.post("/signup")
def register_user(session: SessionDep, user_input:UserRegister)->Any:
    """
    create user without login
    """
    user = get_user_by_username_or_email(session=session, credential=user_input.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_create = UserCreate(user_input)
    new_user = create_user(session=session, user_create=user_create)    
    return new_user
    # try:
    #     user_create = UserCreate.model_validate(user_input)
    #     new_user = create_user(session=session, user_create=user_create)
    #     return new_user
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=str(e),
    #     )
    