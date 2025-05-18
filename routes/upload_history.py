from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import math

from db.database import ExtractionLog
from db.session import get_db
from utils.logger import logger
from utils.config import TEMPLATES_DIR

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/uploads/history", response_class=HTMLResponse)
async def upload_history(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        # Get total count
        total = db.query(ExtractionLog).count()
        total_pages = math.ceil(total / page_size)

        # Validate page number
        if total > 0 and page > total_pages:
            raise HTTPException(status_code=404, detail="Page not found")

        # Calculate offset
        offset = (page - 1) * page_size

        # Get paginated logs
        logs = db.query(ExtractionLog) \
            .order_by(ExtractionLog.upload_time.desc()) \
            .offset(offset) \
            .limit(page_size) \
            .all()

        logger.info(f"📁 Retrieved {len(logs)} upload history entries.")

        return templates.TemplateResponse("upload_history.html", {
            "request": request,
            "logs": logs,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        })

    except Exception as e:
        logger.error(f"Error retrieving upload history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving upload history"
        )