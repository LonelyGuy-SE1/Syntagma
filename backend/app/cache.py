import time
import threading

_lock = threading.Lock()
_cache: dict[str, tuple[float, object]] = {}
DEFAULT_TTL = 60  # seconds


def get(key: str) -> object | None:
    with _lock:
        entry = _cache.get(key)
        if entry is None:
            return None
        ts, value = entry
        if time.monotonic() - ts > DEFAULT_TTL:
            del _cache[key]
            return None
        return value


def put(key: str, value: object, ttl: int = DEFAULT_TTL) -> None:
    with _lock:
        _cache[key] = (time.monotonic(), value)


def invalidate(prefix: str = "") -> None:
    with _lock:
        if not prefix:
            _cache.clear()
            return
        keys = [k for k in _cache if k.startswith(prefix)]
        for k in keys:
            del _cache[k]
