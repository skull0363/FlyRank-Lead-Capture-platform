import httpx, os

PROVIDER_A = os.getenv("GEO_PROVIDER_A_URL", "http://ip-api.com/json/")
PROVIDER_B = os.getenv("GEO_PROVIDER_B_URL", "https://ipapi.co")

def _try_provider_a(ip):
    r = httpx.get(f"{PROVIDER_A}{ip}", timeout=2)
    r.raise_for_status()
    data = r.json()
    return data.get("country"), data.get("city")

def _try_provider_b(ip):
    r = httpx.get(f"{PROVIDER_B}/{ip}/json/", timeout=2)
    r.raise_for_status()
    data = r.json()
    return data.get("country_name"), data.get("city")

def enrich_ip(ip: str):
    if ip in ("127.0.0.1", "localhost", "testclient"):
        return None, None  # nothing to enrich locally
    for provider in (_try_provider_a, _try_provider_b):
        try:
            return provider(ip)
        except Exception:
            continue
    return None, None  # both down — degrade, never fail