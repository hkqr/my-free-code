from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator
import httpx

@dataclass
class ProviderContext:
    provider_id: str
    model: str
    api_key: str
    base_url: str
    timeout: float = 180

class ProviderAdapter(ABC):
    @abstractmethod
    async def complete(self, ctx: ProviderContext, payload: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def stream(self, ctx: ProviderContext, payload: dict) -> AsyncIterator[dict]:
        raise NotImplementedError

class OpenAIChatAdapter(ProviderAdapter):
    async def complete(self, ctx, payload):
        headers = {"Content-Type": "application/json"}
        if ctx.api_key:
            headers["Authorization"] = f"Bearer {ctx.api_key}"
        async with httpx.AsyncClient(timeout=ctx.timeout) as client:
            response = await client.post(
                ctx.base_url.rstrip("/") + "/chat/completions",
                headers=headers,
                json=payload,
            )
        if response.status_code >= 400:
            raise RuntimeError(f"upstream HTTP {response.status_code}: {response.text[:1000]}")
        return response.json()

    async def stream(self, ctx, payload):
        headers = {"Content-Type": "application/json"}
        if ctx.api_key:
            headers["Authorization"] = f"Bearer {ctx.api_key}"
        payload = dict(payload)
        payload["stream"] = True
        async with httpx.AsyncClient(timeout=ctx.timeout) as client:
            async with client.stream(
                "POST",
                ctx.base_url.rstrip("/") + "/chat/completions",
                headers=headers,
                json=payload,
            ) as response:
                if response.status_code >= 400:
                    text = (await response.aread()).decode(errors="replace")
                    raise RuntimeError(f"upstream HTTP {response.status_code}: {text[:1000]}")
                async for line in response.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    value = line[5:].strip()
                    if value == "[DONE]":
                        return
                    try:
                        import json
                        yield json.loads(value)
                    except ValueError:
                        continue

class AnthropicMessagesAdapter(ProviderAdapter):
    """Base for providers exposing Anthropic Messages directly.

    Subclasses only need to implement endpoint-specific authentication or
    small request/response differences.
    """
    async def complete(self, ctx, payload):
        headers = {"Content-Type": "application/json"}
        if ctx.api_key:
            headers["x-api-key"] = ctx.api_key
        headers["anthropic-version"] = "2023-06-01"
        async with httpx.AsyncClient(timeout=ctx.timeout) as client:
            response = await client.post(
                ctx.base_url.rstrip("/") + "/messages",
                headers=headers,
                json=payload,
            )
        if response.status_code >= 400:
            raise RuntimeError(f"upstream HTTP {response.status_code}: {response.text[:1000]}")
        return response.json()

    async def stream(self, ctx, payload):
        raise NotImplementedError("implement provider-specific Anthropic streaming here")
