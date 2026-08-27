import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("JWT_SECRET", "test-secret-for-ci-only")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("CORS_ALLOWED_ORIGINS", "http://localhost:5500")

from app.main import app  # noqa: E402
from app.db import engine  # noqa: E402
from app.models.models import Base, Widget  # noqa: E402

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def _create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def registered_tenant():
    """Registers a fresh tenant and returns (tenant_id, auth_headers)."""
    import uuid
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    resp = client.post("/auth/register", json={
        "name": "Test Tenant",
        "email": email,
        "password": "correct-horse-battery-staple",
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    return body["tenant_id"], {"Authorization": f"Bearer {body['access_token']}"}


@pytest.fixture()
def other_tenant():
    """A second, separate tenant -- used to prove tenant isolation."""
    import uuid
    email = f"other-{uuid.uuid4().hex[:8]}@example.com"
    resp = client.post("/auth/register", json={
        "name": "Other Tenant",
        "email": email,
        "password": "another-strong-password",
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    return body["tenant_id"], {"Authorization": f"Bearer {body['access_token']}"}


@pytest.fixture()
def seeded_widget(registered_tenant):
    _, headers = registered_tenant
    resp = client.post("/widgets", json={
        "type": "signup_form",
        "title": "Test Widget",
        "description": "",
        "fields": [{"name": "email", "type": "email", "required": True}],
        "button_text": "Submit",
        "display_options": {},
    }, headers=headers)
    assert resp.status_code == 201, resp.text
    return resp.json()["widget"]["id"]