from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db import get_db
from app.models.models import Tenant
from app.api.schemas import TenantRegister, TenantLogin
from app.services.auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(body: TenantRegister, db: Session = Depends(get_db)):
    tenant = Tenant(
        name=body.name,
        email=body.email,
        password_hash=hash_password(body.password),
    )
    db.add(tenant)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "An account with this email already exists")
    db.refresh(tenant)

    token = create_token(tenant.id)
    return {"access_token": token, "token_type": "bearer", "tenant_id": tenant.id}


@router.post("/login")
def login(body: TenantLogin, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.email == body.email).first()
    if not tenant or not verify_password(body.password, tenant.password_hash):

        raise HTTPException(401, "Invalid email or password")

    token = create_token(tenant.id)
    return {"access_token": token, "token_type": "bearer", "tenant_id": tenant.id}