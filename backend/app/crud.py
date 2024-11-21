from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from backend.app.models.user import (
    User,
    UserPrivate,
    UserCreate,
    UserRegister,
    UserUpdateInfo,
    UserUpdatePassword,)
from backend.app.core.security import verify_password, get_password_hash

def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

# def get_user_by_id(*, session: Session) -> UserPrivate|None:
#     statement = select

def create_user(*, session: Session, user_create:UserCreate)->User:
    db_user = User.model_validate(
        user_create, update={"hashed_password":get_password_hash(user_create.password)}
    )
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail={"error": "Database error", "message": str(e)},
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail={"error": "Unexpected error", "message": str(e)},
        )
    return db_user
 
def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user