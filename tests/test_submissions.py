from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_oversized_payload_rejected():
    big_data = {"note": "x" * 20000}
    r = client.post("/submissions", json={"widget_id": "w1", "data": big_data})
    assert r.status_code in (413, 400)


def test_missing_required_field():
    r = client.post("/submissions", json={"widget_id": "w1", "data": {}})
    assert r.status_code == 400


def test_honeypot_blocks_spam():
    """UPDATED: honeypot hits now return 200 (the bot must never learn it was
    caught) but are stored with is_spam=True instead of being discarded, so
    this test now also confirms the row exists and is flagged correctly."""
    r = client.post(
        "/submissions",
        json={"widget_id": "w1", "data": {"email": "a@a.com"}, "honeypot": "bot-filled"},
    )
    assert r.status_code == 200
    submission_id = r.json()["id"]

    from app.db import SessionLocal
    from app.models.models import Submission

    db = SessionLocal()
    stored = db.query(Submission).filter(Submission.id == submission_id).first()
    assert stored is not None
    assert stored.is_spam is True
    db.close()


def test_duplicate_idempotency_key_does_not_double_store():
    """NEW: proves the previously-missing idempotency protection actually
    works -- the same Idempotency-Key against the same widget must not
    create two rows."""
    headers = {"Idempotency-Key": "test-key-001"}
    r1 = client.post(
        "/submissions",
        json={"widget_id": "w1", "data": {"email": "dup@test.com"}},
        headers=headers,
    )
    r2 = client.post(
        "/submissions",
        json={"widget_id": "w1", "data": {"email": "dup@test.com"}},
        headers=headers,
    )
    assert r1.json()["id"] == r2.json()["id"]


@patch("app.services.geo._try_provider_a", side_effect=Exception("down"))
@patch("app.services.geo._try_provider_b", return_value=("UK", "London"))
def test_geo_fallback_to_provider_b(mock_b, mock_a):
    from app.services.geo import enrich_ip
    country, city = enrich_ip("8.8.8.8")
    assert country == "UK"


@patch("app.services.geo._try_provider_a", side_effect=Exception("down"))
@patch("app.services.geo._try_provider_b", side_effect=Exception("down"))
def test_all_providers_down_degrades(mock_b, mock_a):
    from app.services.geo import enrich_ip
    country, city = enrich_ip("8.8.8.8")
    assert country is None  

def test_rate_limit_returns_429_on_burst():
    for _ in range(6):
        r = client.post("/submissions", json={"widget_id": "w1", "data": {"email": "a@a.com"}})
    assert r.status_code == 429