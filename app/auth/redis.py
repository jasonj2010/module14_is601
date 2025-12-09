# app/auth/redis.py
"""
Redis blacklist utilities.

This module is written to be *optional* so that the project can run on
environments where `aioredis` (or its deprecated dependencies like
`distutils`) are not available, such as Python 3.13 on the host.

In production/Docker (Python 3.10), `aioredis` will be available and
the real Redis integration will be used. In local tests without
`aioredis`, this module falls back to a no-op in-memory implementation
that satisfies the interface used by the rest of the app.
"""

from __future__ import annotations

import time
from typing import Optional

from app.core.config import settings

# Try very hard *not* to crash if aioredis (or one of its imports) is broken.
try:
    import importlib.util

    spec = importlib.util.find_spec("aioredis")
    if spec is None:
        aioredis = None  # type: ignore[assignment]
    else:  # pragma: no cover - trivial import path
        import aioredis  # type: ignore[import]
except Exception:  # pragma: no cover - we just want to stay alive
    aioredis = None  # type: ignore[assignment]


REDIS_URL: str = getattr(settings, "REDIS_URL", "redis://localhost:6379/0")


class _DummyRedis:
    """
    Minimal in-memory stand-in for Redis, used only when aioredis is unavailable.

    It implements the tiny subset of methods our code uses:
    - setex(key, ttl, value)
    - get(key)
    """

    def __init__(self) -> None:
        self._store: dict[str, tuple[str, float]] = {}

    async def setex(self, key: str, ttl: int, value: str) -> None:
        expires_at = time.time() + max(ttl, 0)
        self._store[key] = (value, expires_at)

    async def get(self, key: str) -> Optional[str]:
        item = self._store.get(key)
        if not item:
            return None
        value, expires_at = item
        if time.time() > expires_at:
            # Expired; remove and behave like a miss
            self._store.pop(key, None)
            return None
        return value


if aioredis:
    # Real Redis client (used in Docker / production)
    redis = aioredis.from_url(REDIS_URL, decode_responses=True)
else:
    # Fallback dummy client (used locally when aioredis can't import)
    redis = _DummyRedis()


async def add_to_blacklist(jti: str, exp_timestamp: int) -> None:
    """
    Store the token's JTI in the blacklist until its expiry.

    In real Redis mode this writes to Redis with TTL.
    In dummy mode it writes to the in-memory store.
    """
    ttl = int(exp_timestamp - time.time())
    ttl = max(ttl, 0)
    key = f"blacklist:{jti}"
    await redis.setex(key, ttl, "true")


async def is_blacklisted(jti: str) -> bool:
    """
    Check if a token JTI is blacklisted.

    In dummy mode this checks the in-memory store.
    """
    key = f"blacklist:{jti}"
    value = await redis.get(key)
    return value == "true"
