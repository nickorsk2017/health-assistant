import asyncio
import time
from dataclasses import dataclass
from typing import Any


@dataclass
class _Entry:
    value: Any
    expires_at: float


class PubMedCache:
    def __init__(self, ttl_seconds: int = 3600) -> None:
        self._store: dict[str, _Entry] = {}
        self._ttl = ttl_seconds
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Any:
        async with self._lock:
            entry = self._store.get(key)
            if entry and time.monotonic() < entry.expires_at:
                return entry.value
            return None

    async def set(self, key: str, value: Any) -> None:
        async with self._lock:
            self._store[key] = _Entry(
                value=value,
                expires_at=time.monotonic() + self._ttl,
            )
