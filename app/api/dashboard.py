from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.api.deps import get_current_tenant
from app.models.models import Submission, Widget, Tenant

router = APIRouter()


@router.get("/dashboard/submissions")
def list_submissions(tenant: Tenant = Depends(get_current_tenant), db: Session = Depends(get_db)):
    return db.query(Submission).filter(Submission.tenant_id == tenant.id).all()


@router.get("/dashboard/stats")
def stats(tenant: Tenant = Depends(get_current_tenant), db: Session = Depends(get_db)):
    total = db.query(func.count(Submission.id)).filter(Submission.tenant_id == tenant.id).scalar()
    spam_count = (
        db.query(func.count(Submission.id))
        .filter(Submission.tenant_id == tenant.id, Submission.is_spam == True) 
        .scalar()
    )

    by_widget = (
        db.query(Submission.widget_id, func.count(Submission.id))
        .filter(Submission.tenant_id == tenant.id, Submission.is_spam == False)  
        .group_by(Submission.widget_id)
        .all()
    )
    by_country = (
        db.query(Submission.country, func.count(Submission.id))
        .filter(Submission.tenant_id == tenant.id, Submission.is_spam == False) 
        .group_by(Submission.country)
        .all()
    )
    return {
        "total": total,
        "spam_blocked": spam_count,
        "by_widget": dict(by_widget),
        "by_country": dict(by_country),
    }