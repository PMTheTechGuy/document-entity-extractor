# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Handles application requests for the web interface.
# ──────────────────────────────────────────────────────────────────────────────
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from typing import List
import os
import json
import asyncio
import time
import csv

# ──────── Custom modules ────────
from utils.logger import logger
from utils.config import CLEANUP_INTERVAL_SECONDS, FILE_EXPIRATION_SECONDS, OUTPUT_FOLDER, LOG_FOLDER, PROJECT_ROOT
from utils.file_cleanup import cleanup_old_files
from db.database import SessionLocal, engine, Base
from routes.upload_routes import router as upload_routes
from routes.results_routes import router as results_routes
from routes.feedback_routes import router as feedback_routes
from routes.upload_history import router as upload_history_routes

# ──────── Load .env variables ────────
load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# App lifecycle context: Initializes folders, warns if API key is missing,
# and starts background file cleanup.
# ──────────────────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting app with lifespan...")
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    LOG_FOLDER.mkdir(exist_ok=True)

    # Initialize database tables
    Base.metadata.create_all(bind=engine)

    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("Waring:⚠️ An OPENAI_API_KEY was not set. GPT extraction will fail if not used.")

    # Start file cleanup task
    asyncio.create_task(cleanup_old_files(OUTPUT_FOLDER, FILE_EXPIRATION_SECONDS, CLEANUP_INTERVAL_SECONDS))
    yield

    logger.info("✅ Lifespan: cleanup complete.")
    yield
    logger.info("🛑 App is shutting down cleanly")

# Initialize FastAPI with a custom lifespan
app = FastAPI(lifespan=lifespan)

# Mount static file
app.mount("/static", StaticFiles(directory=PROJECT_ROOT / "api" / "static" ), name="static")

# ──────── Include Modular route difinitions ────────
app.include_router(upload_routes)
app.include_router(results_routes)
app.include_router(feedback_routes)
app.include_router(upload_history_routes)
