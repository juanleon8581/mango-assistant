import json
import urllib.request
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path


_CACHE_TTL_HOURS = 24
_PACKAGE_NAME = "mango-tui"


def _cache_path() -> Path:
    cache_dir = Path.home() / ".cache" / "mango"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / "update-check.json"


def _fetch_latest_version() -> str | None:
    url = f"https://pypi.org/pypi/{_PACKAGE_NAME}/json"
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            data = json.loads(resp.read())
            return data["info"]["version"]
    except Exception:
        return None


def _is_cache_fresh(cache: dict) -> bool:
    checked_at = cache.get("checked_at")
    if not checked_at:
        return False
    delta = datetime.now(timezone.utc) - datetime.fromisoformat(checked_at)
    return delta.total_seconds() < _CACHE_TTL_HOURS * 3600


def check_for_update() -> None:
    cache_file = _cache_path()
    cache: dict = {}

    if cache_file.exists():
        try:
            cache = json.loads(cache_file.read_text())
        except Exception:
            pass

    if _is_cache_fresh(cache):
        latest = cache.get("latest_version")
    else:
        latest = _fetch_latest_version()
        cache = {
            "latest_version": latest,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            cache_file.write_text(json.dumps(cache))
        except Exception:
            pass

    if not latest:
        return

    current = version(_PACKAGE_NAME)
    if latest != current:
        print(f"  mango update available: {current} → {latest}")
        print(f"  run: pip install --upgrade {_PACKAGE_NAME}\n")
