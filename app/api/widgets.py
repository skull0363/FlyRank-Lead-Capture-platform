from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.api.deps import get_current_tenant
from app.api.schemas import WidgetCreate
from app.models.models import Widget, Tenant

router = APIRouter()


def widget_to_dict(widget: Widget) -> dict:
    return {
        "id": widget.id,
        "tenant_id": widget.tenant_id,
        "type": widget.type,
        "title": widget.title,
        "description": widget.description,
        "fields": widget.fields,
        "button_text": widget.button_text,
        "display_options": widget.display_options,
        "version": widget.version,
        "created_at": widget.created_at.isoformat() if widget.created_at else None,
    }


def _embed_snippet(widget_id: str) -> str:
    return f'<script src="http://localhost:8000/widget.js?id={widget_id}"></script>'


def _get_owned_widget_or_404(db: Session, widget_id: str, tenant: Tenant) -> Widget:
    """FIX: centralizes the tenant-isolation check. Every read/update/delete
    below goes through this so tenant A can never touch tenant B's widget --
    it returns 404, not 403, so an attacker can't even confirm the widget ID
    exists for another tenant."""
    widget = (
        db.query(Widget)
        .filter(Widget.id == widget_id, Widget.tenant_id == tenant.id)
        .first()
    )
    if not widget:
        raise HTTPException(404, "Widget not found")
    return widget


@router.post("/widgets", status_code=201)
def create_widget(
    body: WidgetCreate,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    widget = Widget(tenant_id=tenant.id, **body.dict())
    db.add(widget)
    db.commit()
    db.refresh(widget)
    return {"widget": widget_to_dict(widget), "embed_snippet": _embed_snippet(widget.id)}


@router.get("/widgets")
def list_widgets(
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    """NEW: was missing entirely. Tenant-scoped list of the caller's own widgets."""
    widgets = db.query(Widget).filter(Widget.tenant_id == tenant.id).all()
    return {"widgets": [widget_to_dict(w) for w in widgets]}


@router.get("/widgets/{widget_id}")
def get_widget(
    widget_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    """NEW: was missing entirely."""
    widget = _get_owned_widget_or_404(db, widget_id, tenant)
    return {"widget": widget_to_dict(widget), "embed_snippet": _embed_snippet(widget.id)}


@router.put("/widgets/{widget_id}")
def update_widget(
    widget_id: str,
    body: WidgetCreate,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    """NEW: was missing entirely. Bumps `version` so the cached, versioned
    widget.js/config delivery in delivery.py can correctly cache-bust."""
    widget = _get_owned_widget_or_404(db, widget_id, tenant)
    for field, value in body.dict().items():
        setattr(widget, field, value)
    widget.version += 1
    db.commit()
    db.refresh(widget)
    return {"widget": widget_to_dict(widget)}


@router.delete("/widgets/{widget_id}", status_code=204)
def delete_widget(
    widget_id: str,
    tenant: Tenant = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    """NEW: was missing entirely."""
    widget = _get_owned_widget_or_404(db, widget_id, tenant)
    db.delete(widget)
    db.commit()
    return None