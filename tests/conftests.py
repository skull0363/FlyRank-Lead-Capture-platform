
import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("JWT_SECRET", "test-secret-for-ci-only")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("CORS_ALLOWED_ORIGINS", "http://localhost:5500")

from app.main import app  

client = TestClient(app)


@pytest.fixture()
def registered_tenant():
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