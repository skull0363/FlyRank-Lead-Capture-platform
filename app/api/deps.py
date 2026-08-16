from fastapi import Depends, HTTPException, Header
from app.services.auth import decode_token
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import Tenant

def get_current_tenant(authorization: str = Header(None), db: Session = Depends(get_db)) -> Tenant:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid Authorization header")
    token = authorization.split(" ")[1]
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(401, "Invalid or expired token")
    tenant = db.query(Tenant).filter(Tenant.id == payload["sub"]).first()
    if not tenant:
        raise HTTPException(401, "Tenant not found")
    return tenant