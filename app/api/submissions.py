from fastapi import APIRouter, Depends, HTTPException, Request, Header
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db import get_db
from app.models.models import Widget, Submission
from app.api.schemas import SubmissionCreate
from app.services.geo import enrich_ip
from app.services.notify import send_confirmation

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

MAX_BODY_BYTES = 10_000  


@router.post("/submissions")
@limiter.limit("5/minute") 
async def create_submission(
    payload: SubmissionCreate,
    request: Request,
    db: Session = Depends(get_db),
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
):
    raw = await request.body()
    if len(raw) > MAX_BODY_BYTES:
        raise HTTPException(413, detail={"error": "payload_too_large"})

    widget = db.query(Widget).filter(Widget.id == payload.widget_id).first()
    if not widget:
        raise HTTPException(404, detail={"error": "widget_not_found"})
    if idempotency_key:
        existing = (
            db.query(Submission)
            .filter(Submission.widget_id == widget.id, Submission.idempotency_key == idempotency_key)
            .first()
        )
        if existing:
            return {"status": "ok", "id": existing.id}

    required_names = [f["name"] for f in widget.fields if f.get("required")]
    missing = [n for n in required_names if n not in payload.data or not str(payload.data[n]).strip()]
    if missing:
        raise HTTPException(400, detail={"error": "missing_required_fields", "fields": missing})
    is_spam = bool(payload.honeypot)

    ip = request.client.host
    country, city = (None, None) if is_spam else enrich_ip(ip)

    submission = Submission(
        widget_id=widget.id,
        tenant_id=widget.tenant_id,
        payload=payload.data,
        ip_address=ip,
        country=country,
        city=city,
        is_spam=is_spam,
        idempotency_key=idempotency_key,
    )
    db.add(submission)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = (
            db.query(Submission)
            .filter(Submission.widget_id == widget.id, Submission.idempotency_key == idempotency_key)
            .first()
        )
        return {"status": "ok", "id": existing.id}
    db.refresh(submission)

    if not is_spam:
        try:
            send_confirmation(payload.data.get("email"), widget.title)
        except Exception:
            pass  

    return {"status": "ok", "id": submission.id}