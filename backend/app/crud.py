from sqlmodel import Session, select, or_
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from backend.app.models.user import (
    User,
    UserRoot,
    UserCreate,
    UserRootCreate,
    UserRegister,
    UserUpdateInfo,
    UserUpdatePassword,
)
from backend.app.core.security import verify_password, get_password_hash

def get_user_by_username_or_email(*, session:Session, credential:str) -> User|None:
    """
    retrieve username or email, stop when found one
    """
    query = select(User).where(
        or_(
            User.username == credential,
            User.email == credential,
        )
    )
    session_user = session.exec(query).first()
    return session_user

def create_user(*, session:Session, user_create:UserCreate)->User:
    db_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        address=user_create.address,
    )
    
    if user_create.is_root:
        db_user.is_root = UserRoot(
            is_active=user_create.is_root.is_active,
            is_superuser=user_create.is_root.is_superuser,
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

def create_user_root(*, session:Session, user_root:UserRootCreate)->UserRoot:
    db_user = UserRoot(user_root)
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
 
def authenticate(*, session: Session, credential: str, password: str) -> User|None:
    db_user = get_user_by_username_or_email(session=session, credential=credential)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

def update_user(*, session: Session, db_user: User, user_in: UserUpdatePassword):
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
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