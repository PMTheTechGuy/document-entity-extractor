"""
Author: PM The Tech Guy
Created: 2025-05-08
Purpose: Handles insertion of extraction logs into the database.
"""

from db.database import ExtractionLog
from datetime import datetime
from sqlalchemy.orm import Session
from utils.logger import logger  # The existing logger

def db_log_extraction(
    db: Session,
    filename: str,
    name_count: int,
    email_count: int,
    org_count: int,
    user_ip: str = None
):
    """
    Logs extraction summary to the database.

    Args:
        db (Session): SQLAlchemy session object.
        filename (str): The name of the file.
        name_count (int): Number of names extracted.
        email_count (int): Number of emails extracted.
        org_count (int): Number of orgs extracted.
        user_ip (str): IP address of the requester (optional, for tracking uploads maybe).
    """
    try:
        log_entry = ExtractionLog(
            filename=filename,
            name_count=name_count,
            email_count=email_count,
            org_count=org_count,
            upload_time=datetime.now(),
            user_ip=user_ip
        )
        db.add(log_entry)
        db.commit()
        logger.info(f"✅ Logged extraction to DB for file: {filename}")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Failed to log to DB for file {filename}: {e}")
