from fastapi import APIRouter, Header, HTTPException
from ..config import settings
from ..providers.catalog import PROVIDERS
from ..core.model_catalog import public_catalog

router = APIRouter(prefix="/api/admin")

def auth(value):
    if settings.auth_token and value != f"Bearer {settings.auth_token}":
        raise HTTPException(401, "invalid authorization")

@router.get("/status")
async def status(authorization: str | None = Header(None)):
    auth(authorization)
    return {
        "version": "0.8.0",
        "gateway": "ready",
        "provider_count": len(PROVIDERS),
        "clients": ["claude", "codex", "pi", "opencode", "cline", "hermes", "deepseek-harness", "grok", "muse"],
    }

@router.get("/models")
async def models(authorization: str | None = Header(None)):
    auth(authorization)
    return {"data": public_catalog(settings)}

@router.get("/providers")
async def providers(authorization: str | None = Header(None)):
    auth(authorization)
    return {"data": [{"id": p.id, "name": p.name, "base_url": p.base_url} for p in PROVIDERS]}
