import json
import secrets
import uuid
from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from ..config import settings
from ..core.router import select_model, candidates
from ..core.anthropic import rough_token_count
from ..core.responses import responses_to_messages, messages_to_response
from ..providers.runtime import ProviderRuntime
from ..providers.catalog import PROVIDERS
from .admin_routes import router as admin_router
from ..core.model_catalog import public_catalog

router = APIRouter()
router.include_router(admin_router)
runtime = ProviderRuntime(settings)

def require_auth(authorization: str | None):
    if not settings.auth_token:
        return
    expected = "Bearer " + settings.auth_token
    if not authorization or not secrets.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="invalid proxy authorization")

def loopback_only(host: str | None):
    if host not in {"127.0.0.1", "::1", "localhost"}:
        raise HTTPException(status_code=403, detail="admin is local-only")

@router.get("/health")
async def health():
    return {"status": "ok", "service": "my-free-code", "version": "0.3.0"}

@router.get("/v1/models")
async def list_models(authorization: str | None = Header(None)):
    require_auth(authorization)
    data = []
    for model in {settings.model, settings.fable, settings.opus, settings.sonnet, settings.haiku, *settings.fallbacks}:
        if model and "/" in model:
            data.append({"id": model, "object": "model", "owned_by": model.split("/",1)[0]})
    data.extend({"id": x, "object": "model", "owned_by": "my-free-code"} for x in public_catalog(settings) if x not in {d["id"] for d in data})
    return {"object": "list", "data": data}

@router.post("/v1/messages/count_tokens")
async def count_tokens(body: dict, authorization: str | None = Header(None)):
    require_auth(authorization)
    return {"input_tokens": rough_token_count(body)}

@router.post("/v1/messages")
async def messages(body: dict, authorization: str | None = Header(None)):
    require_auth(authorization)
    selected = select_model(body.get("model"), settings)

    if not body.get("stream"):
        last = None
        for model in candidates(selected, settings):
            try:
                return await runtime.complete(body, model)
            except Exception as exc:
                last = exc
        raise HTTPException(status_code=502, detail=str(last))

    return StreamingResponse(
        stream_messages(body, selected),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )

async def stream_messages(body, selected):
    message_id = "msg_" + uuid.uuid4().hex[:20]
    start = {
        "type": "message_start",
        "message": {
            "id": message_id,
            "type": "message",
            "role": "assistant",
            "content": [],
            "model": selected,
            "stop_reason": None,
            "usage": {"input_tokens": 0, "output_tokens": 0},
        },
    }
    yield f"event: message_start\ndata: {json.dumps(start)}\n\n"
    yield 'event: content_block_start\ndata: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}\n\n'

    started = False
    error = None
    for model in candidates(selected, settings):
        try:
            async for chunk in runtime.stream(body, model):
                delta = ((chunk.get("choices") or [{}])[0].get("delta") or {})
                text = delta.get("content")
                if text:
                    started = True
                    event = {
                        "type": "content_block_delta",
                        "index": 0,
                        "delta": {"type": "text_delta", "text": text},
                    }
                    yield f"event: content_block_delta\ndata: {json.dumps(event)}\n\n"
            error = None
            break
        except Exception as exc:
            error = exc
            if started:
                break

    if error and not started:
        event = {"type":"error","error":{"type":"api_error","message":str(error)}}
        yield f"event: error\ndata: {json.dumps(event)}\n\n"
        return

    yield 'event: content_block_stop\ndata: {"type":"content_block_stop","index":0}\n\n'
    yield 'event: message_delta\ndata: {"type":"message_delta","delta":{"stop_reason":"end_turn"}}\n\n'
    yield 'event: message_stop\ndata: {"type":"message_stop"}\n\n'

@router.post("/v1/responses")
async def responses(body: dict, authorization: str | None = Header(None)):
    require_auth(authorization)
    messages_body = responses_to_messages(body)
    result = await messages(messages_body, authorization)
    if isinstance(result, StreamingResponse):
        return result
    return messages_to_response(result)

@router.get("/admin", response_class=HTMLResponse)
async def admin(host: str | None = Header(None)):
    loopback_only(host or "127.0.0.1")
    return """<!doctype html>
<html><head><meta charset="utf-8"><title>My Free Code</title>
<style>
body{font:15px system-ui;max-width:1100px;margin:30px auto;padding:0 20px}
.card{border:1px solid #ddd;border-radius:12px;padding:18px;margin:15px 0}
pre{background:#f5f5f5;padding:12px;overflow:auto}
</style></head><body>
<h1>My Free Code v0.3</h1>
<div class="card"><b>Gateway:</b> Anthropic Messages + OpenAI Responses</div>
<div class="card"><h2>Routing</h2><pre id="config">loading...</pre></div>
<div class="card"><h2>Provider catalog</h2><pre id="providers">loading...</pre></div>
<script>
async function load(){
 const c=await fetch('/api/config'); document.querySelector('#config').textContent=JSON.stringify(await c.json(),null,2);
 const p=await fetch('/api/providers'); document.querySelector('#providers').textContent=JSON.stringify(await p.json(),null,2);
} load();
</script></body></html>"""

@router.get("/api/config")
async def api_config(authorization: str | None = Header(None)):
    require_auth(authorization)
    return {
        "model": settings.model,
        "fable": settings.fable,
        "opus": settings.opus,
        "sonnet": settings.sonnet,
        "haiku": settings.haiku,
        "fallbacks": settings.fallbacks,
    }

@router.get("/api/providers")
async def api_providers(authorization: str | None = Header(None)):
    require_auth(authorization)
    return [
        {"id": p.id, "name": p.name, "generic_openai_adapter": bool(p.base_url)}
        for p in PROVIDERS
    ]
