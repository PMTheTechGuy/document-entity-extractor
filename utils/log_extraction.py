# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Monitors entity extraction activities by adding a row to a dated CSV
#          file in the logs directory. This aids in auditing, monitoring usage,
#          and debugging.
# ──────────────────────────────────────────────────────────────────────────────

from datetime import datetime
import csv

# ------ Custom modules ------
from utils.config import LOG_FOLDER
from utils.logger import logger

# ──────────────────────────────────────────────────────────────────────────────
# CSV logging for each file processed
# ──────────────────────────────────────────────────────────────────────────────
def log_extraction(filename: str, name_count: int, email_count: int, org_count: int):
    """
    Logs summary data for each processed file to a daily CSV log file.

    Args:
        filename (str): Name of the uploaded file.
        name_count (int): Number of names extracted from the document.
        email_count (int): Number of emails extracted.
        org_count (int): Number of organizations extracted.
    """
    log_filename = f"extractions_{datetime.now().date()}.csv"
    log_path = LOG_FOLDER / log_filename
    file_exists = log_path.exists()

    with open(log_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Timestamp", "Filename", "Names", "Emails", "Organizations"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            filename,
            name_count,
            email_count,
            org_count
        ])
        logger.info(f"<UNK> Writing CSV file at: {log_path}")