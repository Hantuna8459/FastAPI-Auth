from sqlmodel import (
    create_engine,
    Session,
    select,
)
from sqlalchemy.orm import joinedload
from collections.abc import Generator

from ..core.config import settings
from ..models.user import User, UserRoot, UserCreate
from ..crud import create_user, create_user_root

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        
def init_db(session:Session)->None:
    """
    create the first superuser
    """
    query = select(User)\
    .options(joinedload(User.is_root))\
    .where(User.username == settings.FIRST_SUPERUSER)
    
    user = session.exec(query).first()
    
    if not user:
        user_root = UserRoot(
                is_superuser=True,
            )
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_root=user_root,
        )
    user = create_user(session=session, user_create=user_in)