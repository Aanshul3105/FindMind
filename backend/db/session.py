"""Database session management"""
from .models import SessionLocal, engine, init_db
from sqlalchemy.orm import Session
from typing import Generator

def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()