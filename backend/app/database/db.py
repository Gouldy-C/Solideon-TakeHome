from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event
from pathlib import Path
import logging

from app.database.models import init_models

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "ssa_dashboard.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False, "timeout": 60},
    pool_pre_ping=True,
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("PRAGMA busy_timeout=5000;")
    cursor.close()

def init_db() -> None:
    if DB_PATH.exists():
        logger.info(f"Database {DB_PATH} already exists. Skipping creation.")
        return
    init_models()
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)