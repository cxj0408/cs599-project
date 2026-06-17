"""
Redis-backed cache helpers for expensive MCP tool calls.

Only deterministic, high-hit-rate tools should be wrapped here. The wrapper is
deliberately fail-open: if Redis is unavailable, MCP calls continue normally.
"""
from __future__ import annotations

import hashlib
import json
import logging
from typing import Any

from langchain_core.tools import BaseTool, StructuredTool

from config import CONFIG

logger = logging.getLogger(__name__)


class RedisMcpCache:
    """Small async Redis adapter with stable JSON keys and fail-open behavior."""

    def __init__(self) -> None:
        self._client = None
        self._available = CONFIG.cache_enabled
        self._init_error_logged = False

    async def _get_client(self):
        if not self._available:
            return None
        if self._client is not None:
            return self._client

        try:
            from redis import asyncio as redis_asyncio

            self._client = redis_asyncio.from_url(
                CONFIG.redis_url,
                decode_responses=True,
                socket_timeout=CONFIG.redis_socket_timeout,
                socket_connect_timeout=CONFIG.redis_socket_timeout,
            )
            await self._client.ping()
            return self._client
        except Exception as exc:  # pragma: no cover - depends on deployment Redis
            self._available = False
            if not self._init_error_logged:
                logger.warning("Redis MCP cache disabled: %s", exc)
                self._init_error_logged = True
            return None

    @staticmethod
    def _stable_json(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def _dumps_value(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, default=str)

    @staticmethod
    def _loads_value(value: str) -> Any:
        return json.loads(value)

    def build_key(self, tool_name: str, args: dict[str, Any]) -> str:
        raw = self._stable_json(args)
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return f"{CONFIG.redis_key_prefix}:{tool_name}:{digest}"

    async def get(self, tool_name: str, args: dict[str, Any]) -> Any | None:
        client = await self._get_client()
        if client is None:
            return None

        try:
            cached = await client.get(self.build_key(tool_name, args))
            if cached is None:
                return None
            return self._loads_value(cached)
        except Exception as exc:  # pragma: no cover - depends on deployment Redis
            logger.warning("Redis MCP cache read failed for %s: %s", tool_name, exc)
            return None

    async def set(self, tool_name: str, args: dict[str, Any], value: Any) -> None:
        client = await self._get_client()
        if client is None:
            return

        ttl = CONFIG.mcp_cache_ttls.get(tool_name)
        if not ttl or ttl <= 0:
            return

        try:
            await client.setex(
                self.build_key(tool_name, args),
                ttl,
                self._dumps_value(value),
            )
        except Exception as exc:  # pragma: no cover - depends on deployment Redis
            logger.warning("Redis MCP cache write failed for %s: %s", tool_name, exc)

    async def close(self) -> None:
        if self._client is None:
            return
        try:
            await self._client.aclose()
        finally:
            self._client = None


def _normalise_call_args(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Drop LangChain runtime-only values so equivalent tool inputs share a key."""
    return {
        key: value
        for key, value in kwargs.items()
        if key not in {"callbacks", "config", "run_manager"}
    }


def wrap_mcp_tool_with_cache(tool: BaseTool, cache: RedisMcpCache) -> BaseTool:
    """Return a LangChain tool that checks Redis before invoking the MCP tool."""

    async def cached_coroutine(**kwargs: Any) -> Any:
        call_args = _normalise_call_args(kwargs)
        cached = await cache.get(tool.name, call_args)
        if cached is not None:
            return cached

        result = await tool.ainvoke(call_args)
        await cache.set(tool.name, call_args, result)
        return result

    return StructuredTool.from_function(
        coroutine=cached_coroutine,
        name=tool.name,
        description=tool.description,
        args_schema=getattr(tool, "args_schema", None),
        return_direct=getattr(tool, "return_direct", False),
    )
