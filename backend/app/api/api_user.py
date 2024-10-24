from typing import Any

from fastapi import APIRouter, HTTPException

from ..models.user import UserPublic, User
from ..api.dependencies import CurrentUser, SessionDep, TokenDep

router = APIRouter()

@router.get("/profile/{user_id}", response_model=UserPublic)
def get_user(
    user_id:int,
    session: SessionDep,
    current_user: CurrentUser
    ) -> Any:
    user = session.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    return user

    