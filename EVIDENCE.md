
collected 7 items                                          

tests/test_submissions.py::test_oversized_payload_rejected PASSED [ 14%]
tests/test_submissions.py::test_missing_required_field PASSED [ 28%]
tests/test_submissions.py::test_honeypot_blocks_spam PASSED[ 42%]
tests/test_submissions.py::test_duplicate_idempotency_key_does_not_double_store PASSED [ 57%]
tests/test_submissions.py::test_geo_fallback_to_provider_b PASSED [ 71%]
tests/test_submissions.py::test_all_providers_down_degradesPASSED [ 85%]
tests/test_submissions.py::test_rate_limit_returns_429_on_burst PASSED [100%]

==================== warnings summary =====================
.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\ethan\OneDrive\Documents\GitHub\FlyRank Lead Capture platform\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

app\api\schemas.py:19
  C:\Users\ethan\OneDrive\Documents\GitHub\FlyRank Lead Capture platform\app\api\schemas.py:19: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed inV3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    class SubmissionCreate(BaseModel):

tests/test_submissions.py: 12 warnings
  C:\Users\ethan\OneDrive\Documents\GitHub\FlyRank Lead Capture platform\.venv\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Usetimezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

tests/test_submissions.py::test_oversized_payload_rejected
tests/test_submissions.py::test_missing_required_field
tests/test_submissions.py::test_honeypot_blocks_spam
tests/test_submissions.py::test_duplicate_idempotency_key_does_not_double_store
tests/test_submissions.py::test_rate_limit_returns_429_on_burst
  C:\Users\ethan\OneDrive\Documents\GitHub\FlyRank Lead Capture platform\app\services\auth.py:24: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    payload = {"sub": tenant_id, "exp": datetime.utcnow() +timedelta(days=7)}

tests/test_submissions.py::test_oversized_payload_rejected
tests/test_submissions.py::test_missing_required_field
tests/test_submissions.py::test_honeypot_blocks_spam
tests/test_submissions.py::test_duplicate_idempotency_key_does_not_double_store
tests/test_submissions.py::test_rate_limit_returns_429_on_burst
  C:\Users\ethan\OneDrive\Documents\GitHub\FlyRank Lead Capture platform\app\api\widgets.py:51: PydanticDeprecatedSince20: The `dict` method is deprecated; use `model_dump` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    widget = Widget(tenant_id=tenant.id, **body.dict())

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============= 7 passed, 24 warnings in 3.26s ==============