# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Sets up the SQLAlchemy database engine, session maker, and defines the
#          ORM model for storing extraction logs including metadata such as filename,
#          entity counts, and user IP.
# ──────────────────────────────────────────────────────────────────────────────

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# ──────── Custom modules ────────
from utils.config import DATABASE_URL
load_dotenv()

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()

class ExtractionLog(Base):

    __tablename__: str = "extraction_logs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.now())
    name_count = Column(Integer, default=0)
    email_count = Column(Integer, default=0)
    org_count = Column(Integer, default=0)
    user_ip = Column(String, nullable=True)

class Feedback(Base):
    __tablename__: str = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)
    submitted_at = Column(DateTime, default=datetime.now())

# Create the table
Base.metadata.create_all(bind=engine)


