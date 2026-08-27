
=================== test session starts ===================
platform win32 -- Python 3.13.9, pytest-9.1.1, pluggy-1.6.0-- C:\Users\ethan\OneDrive\Documents\GitHub\FlyRank Lead Capture platform\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\ethan\OneDrive\Documents\GitHub\FlyRank Lead Capture platform
plugins: anyio-4.14.2, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 0 items / 1 error                                

========================= ERRORS ==========================
_______ ERROR collecting tests/test_submissions.py ________
tests\test_submissions.py:3: in <module>
    from app.main import app
app\main.py:19: in <module>
    from app.api.submissions import limiter
app\api\submissions.py:7: in <module>
    from app.db import get_db
app\db.py:7: in <module>
    engine = create_engine(os.getenv("DATABASE_URL"))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<string>:2: in create_engine
    ???
.venv\Lib\site-packages\sqlalchemy\util\deprecations.py:281: in warned
    return fn(*args, **kwargs)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^
.venv\Lib\site-packages\sqlalchemy\engine\create.py:564: increate_engine
    u = _url.make_url(url)
        ^^^^^^^^^^^^^^^^^^
.venv\Lib\site-packages\sqlalchemy\engine\url.py:860: in make_url
    raise exc.ArgumentError(
E   sqlalchemy.exc.ArgumentError: Expected string or URL object, got None
==================== warnings summary =====================
.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\ethan\OneDrive\Documents\GitHub\FlyRank Lead Capture platform\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

.venv\Lib\site-packages\_pytest\cacheprovider.py:469
  C:\Users\ethan\OneDrive\Documents\GitHub\FlyRank Lead Capture platform\.venv\Lib\site-packages\_pytest\cacheprovider.py:469: PytestCacheWarning: could not create cache path C:\Users\ethan\OneDrive\Documents\GitHub\FlyRank Lead Capture platform\.pytest_cache\v\cache\nodeids: [WinError 5] Access isdenied: 'C:\\Users\\ethan\\OneDrive\\Documents\\GitHub\\FlyRank Lead Capture platform\\pytest-cache-files-7k3sdj5q' -> 'C:\\Users\\ethan\\OneDrive\\Documents\\GitHub\\FlyRank LeadCapture platform\\.pytest_cache'
    config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================= short test summary info =================
ERROR tests/test_submissions.py - sqlalchemy.exc.ArgumentError: Expected string or URL ob...
!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!
============== 2 warnings, 1 error in 4.75s ===============
(.venv) 