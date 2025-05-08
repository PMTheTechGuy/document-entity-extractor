# ───────────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Defines routes for uploading documents and extracting entity data such
#          as names, emails, and organizations. It handles file saving, processing,
#          Excel and CSV exports, as well as logging extractions into both CSV and
#          the database.
# ───────────────────────────────────────────────────────────────────────────────────

from fastapi import APIRouter, Request, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime
from typing import List
import shutil
import os
import json

# ──────── Custom modules ────────
from extractor.text_extractor import extract_info
from extractor.file_reader import read_file
from utils.export_excel import export_to_file
from utils.logger import logger
from utils.config import OUTPUT_FOLDER, TEMPLATES_DIR
from db.database import ExtractionLog
from db.session import get_db


# Set up template rendering
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Create router
router = APIRouter()

# ──────────────────────────────────────────────────────────────────────────────
# Route: GET "/" — Displays the upload form - Homepage
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

# ──────────────────────────────────────────────────────────────────────────────
# Route: POST "/upload/" — Handles file upload and Processing
# ──────────────────────────────────────────────────────────────────────────────
@router.post("/upload/")
async def handle_upload(
    request: Request,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        extracted_rows = []

        for file in files:
            if file.content_type not in [
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "text/plain"
            ]:
                continue

            saved_path = OUTPUT_FOLDER / f"uploaded_{timestamp}_{file.filename}"
            with open(saved_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            if os.path.getsize(saved_path) == 0:
                continue

            text = read_file(str(saved_path))
            result = extract_info(text)

            extracted_rows.append({
                "Filename": file.filename,
                "Source Type": Path(file.filename).suffix,
                "Names": ", ".join(result.get("person", [])),
                "Emails": ", ".join(result.get("email", [])),
                "Organizations": ", ".join(result.get("organization", []))
            })

            db.add(ExtractionLog(
                filename=file.filename,
                name_count=len(result.get("person", [])),
                email_count=len(result.get("email", [])),
                org_count=len(result.get("organization", [])),
                user_ip=request.client.host
            ))

        db.commit()

        if not extracted_rows:
            raise ValueError("No valid or extractable files uploaded.")

        output_base = OUTPUT_FOLDER / f"entities_combined_{timestamp}"
        export_to_file(extracted_rows, str(output_base.with_suffix(".xlsx")), format="xlsx")
        export_to_file(extracted_rows, str(output_base.with_suffix(".csv")), format="csv")

        with open(output_base.with_suffix('.json'), 'w', encoding='utf-8') as f:
            json.dump({
                "files_processed": len(files),
                "names_extracted": sum(len(row["Names"].split(", ")) for row in extracted_rows),
                "emails_extracted": sum(len(row["Emails"].split(", ")) for row in extracted_rows),
                "orgs_extracted": sum(len(row["Organizations"].split(", ")) for row in extracted_rows),
                "results": extracted_rows
            }, f)

        return RedirectResponse(url=f"/results/{output_base.stem}", status_code=303)

    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": str(e)
        }, status_code=400)


