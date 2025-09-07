from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path as path

DB_PATH = path(__file__).parent / "ssa_dashboard.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)