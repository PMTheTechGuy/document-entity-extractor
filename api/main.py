from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import shutil
import os
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from urllib.parse import quote

# Your existing extraction logic
from extractor.text_extractor import extract_info
from utils.export_excel import export_to_excel

load_dotenv()

app = FastAPI()

PROJECT_ROOT = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "templates"))
OUTPUT_FOLDER = PROJECT_ROOT.parent / os.getenv("OUTPUT_FOLDER")
OUTPUT_FOLDER.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})


@app.post("/upload/")
async def handle_upload(request: Request, file: UploadFile = File(...)):
    try:
        if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Unsupported file type.")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        saved_path = OUTPUT_FOLDER / f"uploaded_{timestamp}_{file.filename}"

        # Save file
        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Check if file is empty
        if os.path.getsize(saved_path) == 0:
            raise ValueError("Uploaded file is empty.")

        # Read and extract
        from extractor.file_reader import read_file
        text = read_file(str(saved_path))
        result = extract_info(text)

        names = ", ".join(result.get("person", []))
        emails = ", ".join(result.get("email", []))
        orgs = ", ".join(result.get("organization", []))

        # Save output
        output_excel = OUTPUT_FOLDER / f"entities_{timestamp}.xlsx"
        export_to_excel([{
            "Filename": file.filename,
            "Source Type": Path(file.filename).suffix,
            "Names": names,
            "Emails": emails,
            "Organizations": orgs
        }], str(output_excel))

        return RedirectResponse(
            url=f"/success/?filename={output_excel.name}", status_code=303
        )

    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": str(e)
        }, status_code=400)


@app.get("/success/", response_class=HTMLResponse)
async def success_page(request: Request, filename: str):
    download_url = f"/download/{filename}"
    return templates.TemplateResponse("success.html", {
        "request": request,
        "download_url": download_url
    })

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = OUTPUT_FOLDER / filename
    if file_path.exists():
        return FileResponse(path=file_path, filename=filename)
    return {"error": "File not found."}
