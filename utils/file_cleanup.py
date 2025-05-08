# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Provides a background task that periodically deletes expired files
#          (PDF, DOCX, TXT, JSON, XLSX) from the output directory to maintain
#          a clean and efficient file system.
# ──────────────────────────────────────────────────────────────────────────────
import time
import asyncio
from pathlib import Path
from utils.logger import logger

# ──────────────────────────────────────────────────────────────────────────────
# Background task to periodically delete old output files
# ──────────────────────────────────────────────────────────────────────────────
async def cleanup_old_files(output_folder: Path, expiration_seconds: int, cleanup_interval_seconds: int):
    while True:
        now = time.time()
        logger.info("🧹 Running file cleanup...")
        for file in output_folder.glob("*"):
            if file.is_file() and file.suffix in [".xlsx", ".json", ".pdf", ".docx", ".txt"]:
                file_age = now - file.stat().st_mtime
                if file_age > expiration_seconds:
                    logger.info(f"🗑️ Deleting old file: {file.name}")
                    file.unlink()
        await asyncio.sleep(cleanup_interval_seconds)