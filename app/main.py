from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import os

app = FastAPI(title="Embeddable Widget & Lead-Capture Platform")

_raw_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
allowed = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

from app.api.submissions import limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from app.api import auth, widgets, submissions, delivery, dashboard

app.include_router(auth.router)
app.include_router(widgets.router)
app.include_router(submissions.router)
app.include_router(delivery.router)
app.include_router(dashboard.router)