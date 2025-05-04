# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Handles application requests for the web interface.
# ──────────────────────────────────────────────────────────────────────────────
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from typing import List
import shutil
import os
import json
import asyncio
import time
import csv

# Custom modules
from extractor.text_extractor import extract_info
from utils.export_excel import export_to_file

# sys.path.append(str(Path(__file__).resolve().parent.parent))

# Load environment
load_dotenv()

# Lifespan setup
PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_FOLDER = PROJECT_ROOT.parent / os.getenv("OUTPUT_FOLDER", "output")
LOG_FOLDER = PROJECT_ROOT.parent / "logs"

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("🚀 Starting app...")
    print("Lifespan: initializing app resources...")
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    LOG_FOLDER.mkdir(exist_ok=True)

    if not os.getenv("OPENAI_API_KEY"):
        print("Waring: An OPENAI_API_KEY was not set. GPT extraction will fail if not used.")

    # Start file cleanup task
    asyncio.create_task(cleanup_old_files())

    print("Lifespan: app resources initialized.")
    yield

    print("Lifespan: cleanup complete.")
app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory=str(PROJECT_ROOT / "templates"))

# 🧹 Background cleanup settings
CLEANUP_INTERVAL_SECONDS = 600  # every 10 min
FILE_EXPIRATION_SECONDS = 3600  # 1 hour

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

        output_base = OUTPUT_FOLDER / f"entities_combined_{timestamp}"
        excel_path = output_base.with_suffix(".xlsx")
        csv_path = output_base.with_suffix(".csv")

        export_to_file(extracted_rows, str(excel_path), format="xlsx")
        export_to_file(extracted_rows, str(csv_path), format="csv")

        summary_data = {
            "files_processed": len(files),
            "names_extracted": sum(len(row["Names"].split(", ")) for row in extracted_rows),
            "emails_extracted": sum(len(row["Emails"].split(", ")) for row in extracted_rows),
            "orgs_extracted": sum(len(row["Organizations"].split(", ")) for row in extracted_rows),
            "results": extracted_rows
        }

        # Write full summary to JSON
        result_file = output_base.with_suffix('.json')
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f)

        base_filename = output_base.stem
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
        summary_data = json.load(f)

    # Extract and Flatten preview
    data = summary_data.get("results", [])
    names, emails, orgs = [], [], []
    for row in data:
        names.extend(row.get("Names", "").split(", "))
        emails.extend(row.get("Emails", "").split(", "))
        orgs.extend(row.get("Organizations", "").split(", "))

    # ✅ Return the template with all required data
    return templates.TemplateResponse("results.html", {
        "request": request,
        "names": names[:10],
        "emails": emails[:10],
        "orgs": orgs[:10],
        "filename": f"{filename}.xlsx",
        "download_url": f"/download/{filename}.xlsx",
        "summary": {
            "files": summary_data.get("files_processed", 0),
            "names": summary_data.get("names_extracted", 0),
            "emails": summary_data.get("emails_extracted", 0),
            "orgs": summary_data.get("orgs_extracted", 0),
        }
    })

# Download link
@app.get("/download/{filename}")
async def download_file(request: Request, filename: str):
    file_path = OUTPUT_FOLDER / filename

    if file_path.exists():
            return FileResponse(path=file_path, filename=filename)
        # return {"error": "File not found."}

    if not file_path.exists() or not file_path.is_file():
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": f"The file '{filename}' was not found or may have expired."
        }, status_code=404)
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
# if file_path.exists():
#         return FileResponse(path=file_path, filename=filename)
#     return {"error": "File not found."}