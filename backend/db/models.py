"""Database models for FinMind"""
from sqlalchemy import Column, String, Float, Integer, Date, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'
    
    ticker = Column(String(10), primary_key=True)
    name = Column(String(200))
    sector = Column(String(100))
    industry = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class Price(Base):
    __tablename__ = 'prices'
    
    id = Column(Integer, primary_key=True)
    ticker = Column(String(10))
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///finmind.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")