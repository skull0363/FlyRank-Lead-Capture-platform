from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import Widget, Submission
from app.api.schemas import SubmissionCreate
from app.services.geo import enrich_ip
from app.services.notify import send_confirmation

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

MAX_BODY_BYTES = 10_000  # oversized payload guard

@router.post("/submissions")
@limiter.limit("5/minute")  # per-IP rate limit
async def create_submission(payload: SubmissionCreate, request: Request, db: Session = Depends(get_db)):
    raw = await request.body()
    if len(raw) > MAX_BODY_BYTES:
        raise HTTPException(413, detail={"error": "payload_too_large"})

    widget = db.query(Widget).filter(Widget.id == payload.widget_id).first()
    if not widget:
        raise HTTPException(404, detail={"error": "widget_not_found"})

    # Validate required fields defined on the widget are present
    required_names = [f["name"] for f in widget.fields if f.get("required")]
    missing = [n for n in required_names if n not in payload.data or not str(payload.data[n]).strip()]
    if missing:
        raise HTTPException(400, detail={"error": "missing_required_fields", "fields": missing})

    # Honeypot spam check — silently drop
    if payload.honeypot:
        return {"status": "ok"}  # bots see success, nothing is stored

    ip = request.client.host
    country, city = enrich_ip(ip)  # fallback chain lives inside this function

    submission = Submission(
        widget_id=widget.id,
        tenant_id=widget.tenant_id,
        payload=payload.data,
        ip_address=ip,
        country=country,
        city=city,
    )
    db.add(submission)
    db.commit()

    try:
        send_confirmation(payload.data.get("email"), widget.title)
    except Exception:
        pass  # side-effect failure must never break the main path

    return {"status": "ok", "id": submission.id}