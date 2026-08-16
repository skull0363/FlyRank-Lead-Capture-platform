from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()

def gen_id():
    return str(uuid.uuid4())

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(String, primary_key=True, default=gen_id)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    widgets = relationship("Widget", back_populates="tenant")

class Widget(Base):
    __tablename__ = "widgets"
    id = Column(String, primary_key=True, default=gen_id)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    type = Column(String, nullable=False)         # signup_form | cta | popover
    title = Column(String, nullable=False)
    description = Column(String, default="")
    fields = Column(JSON, nullable=False)          # [{"name": "email", "type": "email", "required": true}]
    button_text = Column(String, default="Submit")
    display_options = Column(JSON, default={})
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    tenant = relationship("Tenant", back_populates="widgets")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(String, primary_key=True, default=gen_id)
    widget_id = Column(String, ForeignKey("widgets.id"), nullable=False)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    payload = Column(JSON, nullable=False)
    ip_address = Column(String)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    is_spam = Column(Boolean, default=False)
    idempotency_key = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)