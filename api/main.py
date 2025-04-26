# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Handles application requests for the web interface.
# ──────────────────────────────────────────────────────────────────────────────

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import quote
from typing import List
import shutil
import logging
import os
import json
import asyncio
import time
import csv

# Custom modules
from extractor.text_extractor import extract_info
from training.label_converter import PROJECT_ROOT
from utils.export_excel import export_to_excel

sys.path.append(str(Path(__file__).resolve().parent.parent))

# Load environment
load_dotenv()
app = FastAPI()

# Logging setup
PROJECT_ROOT = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "templates"))
OUTPUT_FOLDER = PROJECT_ROOT.parent / os.getenv("OUTPUT_FOLDER")
OUTPUT_FOLDER.mkdir(exist_ok=True)
LOG_FOLDER = PROJECT_ROOT.parent / "logs"
LOG_FOLDER.mkdir(exist_ok=True)


# 🧹 Background cleanup settings
CLEANUP_INTERVAL_SECONDS = 600  # every 10 min
FILE_EXPIRATION_SECONDS = 3600  # 1 hour

# Home page
@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

# Upload & process
@app.post("/upload/")
async def handle_upload(request: Request, files: List[UploadFile] = File(...)):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        extracted_rows = []

        for file in files:
            allowed_types = [
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "text/plain"
            ]
            if file.content_type not in allowed_types:
                continue

            saved_path = OUTPUT_FOLDER / f"uploaded_{timestamp}_{file.filename}"
            with open(saved_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            if os.path.getsize(saved_path) == 0:
                continue

            from extractor.file_reader import read_file
            text = read_file(str(saved_path))
            result = extract_info(text)

            extracted_rows.append({
                "Filename": file.filename,
                "Source Type": Path(file.filename).suffix,
                "Names": ", ".join(result.get("person", [])),
                "Emails": ", ".join(result.get("email", [])),
                "Organizations": ", ".join(result.get("organization", []))
            })

            log_extraction(
                filename=file.filename,
                name_count=len(result.get("person", [])),
                email_count=len(result.get("email", [])),
                org_count=len(result.get("organization", []))
            )

        if not extracted_rows:
            raise ValueError("No valid or extractable files uploaded.")

        output_excel = OUTPUT_FOLDER / f"entities_combined_{timestamp}.xlsx"
        export_to_excel(extracted_rows, str(output_excel))

        result_file = output_excel.with_suffix('.json')
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_rows, f)

        base_filename = output_excel.stem
        return RedirectResponse(url=f"/results/{base_filename}", status_code=303)

    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": str(e)
        }, status_code=400)

# Result preview
@app.get("/results/{filename}", response_class=HTMLResponse)
async def show_results(request: Request, filename: str):
    json_path = OUTPUT_FOLDER / f"{filename}.json"
    if not json_path.exists():
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "No results found. The data may have expired or been removed."
        }, status_code=404)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Flatten preview
    names, emails, orgs = [], [], []
    for row in data:
        names.extend(row.get("Names", "").split(", "))
        emails.extend(row.get("Emails", "").split(", "))
        orgs.extend(row.get("Organizations", "").split(", "))

    return templates.TemplateResponse("results.html", {
        "request": request,
        "names": names[:10],
        "emails": emails[:10],
        "orgs": orgs[:10],
        "download_url": f"/download/{filename}.xlsx"
    })

# Download link
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = OUTPUT_FOLDER / filename
    if file_path.exists():
        return FileResponse(path=file_path, filename=filename)
    return {"error": "File not found."}

# Background file cleanup
async def cleanup_old_files():
    while True:
        now = time.time()
        print("🧹 Running file cleanup...")
        for file in OUTPUT_FOLDER.glob("*"):
            if file.is_file() and file.suffix in [".xlsx", ".json", ".pdf", ".docx", ".txt"]:
                file_age = now - file.stat().st_mtime
                if file_age > FILE_EXPIRATION_SECONDS:
                    print(f"🗑️ Deleting old file: {file.name}")
                    file.unlink()
        await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_old_files())


def log_extraction(filename: str, name_count: int, email_count: int, org_count: int):
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