import json
import os
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
    if mock := os.environ.get("MANGO_MOCK_LATEST_VERSION"):
        return mock
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


def _version_tuple(v: str) -> tuple[int, ...]:
    try:
        return tuple(int(x) for x in v.split("."))
    except ValueError:
        return (0,)


def check_for_update() -> tuple[str, str] | None:
    """Returns (current, latest) if a newer version is available, else None."""
    cache_file = _cache_path()
    cache: dict = {}

    if cache_file.exists():
        try:
            cache = json.loads(cache_file.read_text())
        except Exception:
            pass

    if _is_cache_fresh(cache):
        # Cache is only written when an update was found, so this is a hit.
        latest = cache.get("latest_version")
        if not latest:
            return None
        current = version(_PACKAGE_NAME)
        if _version_tuple(latest) > _version_tuple(current):
            return (current, latest)
        # User updated since the cache was written — clear it.
        try:
            cache_file.unlink(missing_ok=True)
        except Exception:
            pass
        return None

    latest = _fetch_latest_version()
    if not latest:
        return None

    current = version(_PACKAGE_NAME)
    if _version_tuple(latest) > _version_tuple(current):
        # Cache the pending update so we don't re-fetch on every launch.
        try:
            cache_file.write_text(
                json.dumps({"latest_version": latest, "checked_at": datetime.now(timezone.utc).isoformat()})
            )
        except Exception:
            pass
        return (current, latest)

    # Up to date — delete any stale cache so we re-check next launch.
    try:
        cache_file.unlink(missing_ok=True)
    except Exception:
        pass
    return None
