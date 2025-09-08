from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path
import logging

from database.models import init_models

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "ssa_dashboard.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

def init_db() -> None:
    if DB_PATH.exists():
        logger.info(f"Database {DB_PATH} already exists. Skipping creation.")
        return
    init_models()
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)



def test_db() -> None:
    from sqlmodel import select
    from database.models import WeldGroup
    
    init_db()
    with get_session() as session:
        weldgroups = session.exec(select(WeldGroup)).all()
        print(weldgroups)