import asyncio, time
from collections import deque
from .catalog import PROVIDER_MAP
from .adapters import OpenAIChatAdapter, ProviderContext
from .specialized import SPECIALIZED
from ..config import Settings
from ..core.anthropic import anthropic_to_openai, openai_to_anthropic
from ..core.failures import classify_status

class ProviderRuntime:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.semaphores = {p.id: asyncio.Semaphore(settings.max_concurrency) for p in PROVIDER_MAP.values()}
        self.calls = {p.id: deque() for p in PROVIDER_MAP.values()}
        self.unhealthy_until = {}

    def context(self, provider_id, remote_model):
        p = PROVIDER_MAP[provider_id]
        base = p.base_url
        if provider_id == "ollama":
            base = self.settings.key("OLLAMA_BASE_URL") or base
        elif provider_id == "lmstudio":
            base = self.settings.key("LM_STUDIO_BASE_URL") or base
        elif provider_id == "llamacpp":
            base = self.settings.key("LLAMACPP_BASE_URL") or base
        if not base:
            raise RuntimeError(f"{p.name} requires a specialized adapter")
        return ProviderContext(provider_id, remote_model, self.settings.key(p.key), base, self.settings.http_timeout)

    def adapter(self, provider_id):
        return SPECIALIZED.get(provider_id, OpenAIChatAdapter)()

    async def admit(self, provider_id):
        now = time.monotonic()
        if now < self.unhealthy_until.get(provider_id, 0):
            raise RuntimeError(f"provider {provider_id} is in recovery backoff")
        q = self.calls[provider_id]
        while q and now - q[0] > self.settings.rate_window:
            q.popleft()
        if len(q) >= self.settings.rate_limit:
            await asyncio.sleep(max(0.01, self.settings.rate_window - (now - q[0])))
        q.append(time.monotonic())
        return self.semaphores[provider_id]

    async def complete(self, anthropic_body, public_model):
        provider_id, remote = public_model.split("/", 1)
        sem = await self.admit(provider_id)
        async with sem:
            adapter = self.adapter(provider_id)
            try:
                data = await adapter.complete(self.context(provider_id, remote),
                                              anthropic_to_openai(anthropic_body, remote))
            except Exception as exc:
                self.unhealthy_until[provider_id] = time.monotonic() + 2
                raise
            return openai_to_anthropic(data, public_model)

    async def stream(self, anthropic_body, public_model):
        provider_id, remote = public_model.split("/", 1)
        sem = await self.admit(provider_id)
        await sem.acquire()
        try:
            adapter = self.adapter(provider_id)
            async for item in adapter.stream(
                self.context(provider_id, remote),
                anthropic_to_openai(anthropic_body, remote)
            ):
                yield item
        except Exception:
            self.unhealthy_until[provider_id] = time.monotonic() + 2
            raise
        finally:
            sem.release()
