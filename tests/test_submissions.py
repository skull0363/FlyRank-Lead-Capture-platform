
from unittest.mock import patch
from tests.conftest import client


def test_oversized_payload_rejected(seeded_widget):
    big_data = {"note": "x" * 20000}
    r = client.post("/submissions", json={"widget_id": seeded_widget, "data": big_data})
    assert r.status_code in (413, 400)


def test_missing_required_field(seeded_widget):
    r = client.post("/submissions", json={"widget_id": seeded_widget, "data": {}})
    assert r.status_code == 400


def test_honeypot_blocks_spam(seeded_widget):
    r = client.post(
        "/submissions",
        json={"widget_id": seeded_widget, "data": {"email": "a@a.com"}, "honeypot": "bot-filled"},
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


def test_duplicate_idempotency_key_does_not_double_store(seeded_widget):
    headers = {"Idempotency-Key": "test-key-001"}
    r1 = client.post(
        "/submissions",
        json={"widget_id": seeded_widget, "data": {"email": "dup@test.com"}},
        headers=headers,
    )
    r2 = client.post(
        "/submissions",
        json={"widget_id": seeded_widget, "data": {"email": "dup@test.com"}},
        headers=headers,
    )
    assert r1.status_code == 200
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
    assert country is None  # succeeds without geo, doesn't raise


def test_rate_limit_returns_429_on_burst(seeded_widget):
    for _ in range(6):
        r = client.post("/submissions", json={"widget_id": seeded_widget, "data": {"email": "a@a.com"}})
    assert r.status_code == 429