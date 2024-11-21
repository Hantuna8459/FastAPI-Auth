from sqlmodel import (
    create_engine,
    Session,
    select,
)
from sqlalchemy.orm import selectinload
from collections.abc import Generator

from ..core.config import settings
from ..models.user import User, UserCreate, UserRoot
from ..crud import create_user

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        
def init_db(session:Session)->None:
    """
    create the first superuser
    """
    stmt = select(User)\
    .where(User.username == settings.FIRST_SUPERUSER)\
    .options(selectinload(User.is_root))
    
    result = session.exec(stmt)
    user = result.first()
    
    if not user:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_root=UserRoot(
                is_superuser=True,
            ),
        )
    user = create_user(session=session, user_create=user_in)

# with Session(engine) as session:
#     # Query with joinedload to eagerly load the related Profile data
#     query = select(User).options(joinedload(User.is_root))
#     users = session.exec(query).all()

#     for user in users:
#         print(f"Username: {user.username}, Root: {user.is_root.is_superuser}")