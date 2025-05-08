# ──────────────────────────────────────────────────────────────────────────────
# Author: Paul-Michael Smith
# Purpose: Manages result-related routes, including displaying extraction
#          summaries and providing download links for Excel/CSV output.
#          It also supports user-friendly viewing of processed entity data.
# ──────────────────────────────────────────────────────────────────────────────

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import json

# ──────── Custom modules ────────
from utils.logger import logger
from utils.config import OUTPUT_FOLDER, TEMPLATES_DIR

# Set up template rendering
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Create router
router = APIRouter()

# ──────────────────────────────────────────────────────────────────────────────
# Route: GET "/results/{filename}" — Displays results summary on webpage
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/results/{filename}", response_class=HTMLResponse)
async def show_results(request: Request, filename: str):
    json_path = OUTPUT_FOLDER / f"{filename}.json"
    logger.info(f"🔎 Looking for JSON file at: {json_path}")

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

    # Return the template with all required data
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


# ──────────────────────────────────────────────────────────────────────────────
# Route: GET "/download/{filename}" — File download
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/download/{filename}")
async def download_file(request: Request, filename: str):
    file_path = OUTPUT_FOLDER / filename

    if file_path.exists():
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type="application/octet-stream",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
    return templates.TemplateResponse("error.html", {
        "request": request,
        "error_message": f"The file '{filename}' was not found or may have expired."
    }, status_code=404)