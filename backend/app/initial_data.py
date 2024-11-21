import logging

from sqlmodel import Session

from backend.app.core.db_connect import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init()->None:
    with Session(engine) as session:
        init_db(session)
        
def main()->None:
    init()
    logger.info("Initial data created")
    
if __name__ == "__main__":
    main()