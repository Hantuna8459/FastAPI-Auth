from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# this one was from sqlalchemy
# def get_db() -> Generator:
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()

def get_session():
    with Session(engine) as session:
        yield session


    
