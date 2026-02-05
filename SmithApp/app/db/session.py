from core.database import SessionLocal
from sqlalchemy.orm import Session

def get_session() -> Session:
    """Get a new database session"""
    return SessionLocal()


def close_session(session: Session) -> None:
    """Close a database session"""
    if session:
        session.close()