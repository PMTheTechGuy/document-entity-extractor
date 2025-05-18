# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Manages the environment variable that allows switching between the SpaCy model and the OpenAI model (using an API key).
# ──────────────────────────────────────────────────────────────────────────────

import os
from pathlib import Path
from dotenv import load_dotenv

# ──────── Load .env variables ────────
load_dotenv()

# Base directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Output folder
OUTPUT_FOLDER = PROJECT_ROOT / "output"

# Log folder
LOG_FOLDER = PROJECT_ROOT / "logs"


# Set up template rendering
TEMPLATES_DIR = PROJECT_ROOT / "api" / "templates"

# SQLite database setup
DATABASE_PATH = PROJECT_ROOT / "db" / "extraction_logs.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# 🧹 Cleanup configuration
CLEANUP_INTERVAL_SECONDS = 600  # every 10 min
FILE_EXPIRATION_SECONDS = 3600  # 1 hour


def use_gpt_extraction():
    return os.getenv("USE_GPT_EXTRACTION", "False").lower() == "true"
