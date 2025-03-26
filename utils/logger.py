"""
Author: PM The Tech Guy
Created: 2025-03-25
Purpose: Main logging script handling configuration of the application.
"""

import logging
import os

# Create logs folder if not exists
os.makedirs("logs", exist_ok=True)

# Configure the logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers = [
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

# Usage: for utils.logger import logger
logger = logging.getLogger(__name__)

# Usage: for logs to appear in terminal for development
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)