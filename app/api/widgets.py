from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.api.deps import get_current_tenant
from app.api.schemas import WidgetCreate
from app.models.models import Widget, Tenant

router = APIRouter()

@router.post("/widgets")
def create_widget(body: WidgetCreate, tenant: Tenant = Depends(get_current_tenant), db: Session = Depends(get_db)):
    widget = Widget(tenant_id=tenant.id, **body.dict())
    db.add(widget); db.commit(); db.refresh(widget)
    return {"widget": widget_to_dict(widget), "embed_snippet": f'<script src="http://localhost:8000/widget.js?id={widget.id}"></script>'}

@router.get("/widgets")
def list_widgets(tenant: Tenant = Depends(get_current_tenant), db: Session = Depends(get_db)):
    return db.query(Widget).filter(Widget.tenant_id == tenant.id).all()

@router.get("/widgets/{widget_id}")
def get_widget(widget_id: str, tenant: Tenant = Depends(get_current_tenant), db: Session = Depends(get_db)):
    w = db.query(Widget).filter(Widget.id == widget_id, Widget.tenant_id == tenant.id).first()
    if not w: raise HTTPException(404, "not found")
    return w

@router.put("/widgets/{widget_id}")
def update_widget(widget_id: str, body: WidgetCreate, tenant: Tenant = Depends(get_current_tenant), db: Session = Depends(get_db)):
    w = db.query(Widget).filter(Widget.id == widget_id, Widget.tenant_id == tenant.id).first()
    if not w: raise HTTPException(404, "not found")
    for k, v in body.dict().items(): setattr(w, k, v)
    w.version += 1
    db.commit()
    return w

@router.delete("/widgets/{widget_id}")
def delete_widget(widget_id: str, tenant: Tenant = Depends(get_current_tenant), db: Session = Depends(get_db)):
    w = db.query(Widget).filter(Widget.id == widget_id, Widget.tenant_id == tenant.id).first()
    if not w: raise HTTPException(404, "not found")
    db.delete(w); db.commit()
    return {"status": "deleted"}

def widget_to_dict(w):
    return {"id": w.id, "title": w.title, "type": w.type}