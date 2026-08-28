import os 
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8082"))
    auth_token: str = os.getenv("PROXY_AUTH_TOKEN", "local")
    model: str = os.getenv("MODEL", "open_router/openrouter/free")
    fable: str = os.getenv("MODEL_FABLE", "")
    opus: str = os.getenv("MODEL_OPUS", "")
    sonnet: str = os.getenv("MODEL_SONNET", "")
    haiku: str = os.getenv("MODEL_HAIKU", "")
    fallbacks: list[str] = field(default_factory=lambda: [
        x.strip() for x in os.getenv("FALLBACK_MODELS", "").split(",") if x.strip()
    ])
    max_concurrency: int = int(os.getenv("PROVIDER_MAX_CONCURRENCY", "5"))
    rate_limit: int = int(os.getenv("PROVIDER_RATE_LIMIT", "10"))
    rate_window: float = float(os.getenv("PROVIDER_RATE_WINDOW", "3"))
    http_timeout: float = float(os.getenv("HTTP_TIMEOUT", "180"))

    def key(self, env_name: str | None) -> str:
        return os.getenv(env_name, "").strip() if env_name else ""

settings = Settings()
