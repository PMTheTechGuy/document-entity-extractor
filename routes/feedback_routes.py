from fastapi import APIRouter, Request, Form, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

# ──────── Custom modules ────────
from utils.logger import logger
from utils.config import TEMPLATES_DIR
from db.session import get_db
from db.database import Feedback

router = APIRouter()

# Set up template
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/feedback", response_class=HTMLResponse)
async def show_feedback_form(request: Request):
    return templates.TemplateResponse("feedback_form.html", context={"request": request})

@router.post("/feedback/submit")
async def submit_feedback(
        request: Request,
        message: str = Form(...),
        rating: int = Form(None),
        db: Session = Depends(get_db)
):
    try:
        feedback = Feedback(message=message, rating=rating, submitted_at=datetime.now())
        db.add(feedback)
        db.commit()
        logger.info(f"📝 New feedback submitted.")
        return RedirectResponse(url="/feedback/thanks", status_code=303)
    except Exception as e:
        logger.error(f"❌ Error saving new feedback: {e}")
        return templates.TemplateResponse("error.html", context={
            "request": request,
            "error_message": "There was an issue submitting your feedback."
        }, status_code=500)

@router.get("/feedback/thanks", response_class=HTMLResponse)
async def thanks_page(request: Request):
    return templates.TemplateResponse("thanks.html", context={"request": request})

@router.get("/feedback/view", response_class=HTMLResponse)
async def view_feedback(
        request: Request,
        db: Session = Depends(get_db),
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        sort_by: str = Query("submitted_at"),
        order: str = Query("desc")

):
    valid_sort = {"submitted_at": Feedback.submitted_at, "rating": Feedback.rating}
    sort_column = valid_sort.get(sort_by, Feedback.submitted_at)
    sort_method = desc(sort_column) if order == "desc" else sort_column

    total = db.query(Feedback).count()
    feedback_entries = (
        db.query(Feedback)
        .order_by(sort_method)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    logger.info(f"Loaded {len(feedback_entries)} feedback entries.")

    return templates.TemplateResponse("feedback_viewer.html", context={
        "request": request,
        "feedback_entries": feedback_entries,
        "page": page,
        "limit": limit,
        "total": total,
        "sort_by": sort_by,
        "order": order
    })