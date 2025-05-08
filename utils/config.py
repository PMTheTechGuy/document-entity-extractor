# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Manages the environment variable that allows switching between the SpaCy model and the OpenAI model (using an API key).
# ──────────────────────────────────────────────────────────────────────────────

import os
from pathlib import Path
from dotenv import load_dotenv

# ──────── Load .env variables ────────
load_dotenv()

# SQLite database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db/extraction_logs.db")

# Output folder
OUTPUT_FOLDER = Path(os.getenv("OUTPUT_FOLDER", "output"))

# Log folder
LOG_FOLDER = Path(os.getenv("LOG_FOLDER", "logs"))

# 🧹 Cleanup configuration
CLEANUP_INTERVAL_SECONDS = 600  # every 10 min
FILE_EXPIRATION_SECONDS = 3600  # 1 hour

# Set up template rendering
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "api" / "templates"

def use_gpt_extraction():
    return os.getenv("USE_GPT_EXTRACTION", "False").lower() == "true"
