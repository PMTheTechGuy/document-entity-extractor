"""
Author: PM The Tech Guy
Created: 2025-03-25
Purpose: Main logging script handling configuration of the application.
"""

import logging
from utils.config import LOG_FOLDER
from pathlib import Path

# Create a logs folder if none exists
Path(LOG_FOLDER).mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_FOLDER / "app.log"

# Configure the logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers = [
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Usage: for utils.logger import logger
logger = logging.getLogger(__name__)

# Usage: for logs to appear in terminal for development
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')
# console.setFormatter(formatter)
# logger.addHandler(console)