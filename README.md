# My Free Code v0.8

**A from-scratch multi-provider gateway for Claude Code and other coding agents.**

This release takes the v0.3 prototype and turns it into a substantially more useful gateway: protocol conversion, model routing, fallback, provider profiles, reasoning metadata, streaming, tools/images, model discovery, local providers, authentication, admin APIs and launcher abstractions.

It is an independent implementation. It is **not affiliated with Anthropic and is not a fork of Free Claude Code**.

## What v0.8 includes

### Gateway protocols
- Anthropic Messages: `/v1/messages`
- Anthropic token counting: `/v1/messages/count_tokens`
- OpenAI Responses-compatible: `/v1/responses`
- model discovery: `/v1/models`
- health: `/health`
- local Admin UI: `/admin`
- authenticated Admin API: `/api/admin/*`

### Agent features
- streaming SSE
- tool definitions and tool calls
- tool results
- images
- reasoning/thinking metadata pass-through
- Claude tier routing: Fable / Opus / Sonnet / Haiku
- no-thinking gateway IDs
- ordered model fallback
- provider health backoff
- per-provider concurrency
- rate-window control
- stable public model identity

### Provider layer
The catalog contains the broad provider set used by the project:

NVIDIA NIM, OpenRouter, Groq, OpenAI, xAI, QwenCloud, Together, DeepInfra, SiliconFlow, Nebius, Chutes, Featherless, ZenMux, W&B Inference, Azure OpenAI, Google AI Studio, Google Vertex, DeepSeek, Mistral, Codestral, OpenCode Zen, OpenCode Go, Vercel AI Gateway, Amazon Bedrock, Hugging Face, Cohere, GitHub Models, Wafer, Kimi, Kimi Code, MiniMax, Cerebras, SambaNova, Kilo, Fireworks, Novita, Cloudflare Workers AI, Z.ai, TokenRouter, NaraRoute, Poolside, LLM7, Ollama Cloud, LM Studio, llama.cpp and Ollama.

Provider entries are not fake claims of universal support: providers with unusual authentication/protocols require a dedicated adapter. The common OpenAI-compatible providers use the shared transport.

### Coding-agent launcher layer
The architecture has launcher adapters for:

- Claude Code
- Codex
- Pi
- OpenCode
- Cline
- Hermes
- DeepSeek Harness
- Grok Build
- Muse Code

A launcher simply prepares the local proxy environment and delegates arguments to the installed client. It never impersonates the provider or bypasses provider authentication.

## Architecture

```text
             Coding Agents / IDEs
                      |
          +-----------+-----------+
          |                       |
    Anthropic Messages       OpenAI Responses
          |                       |
          +-----------+-----------+
                      |
                FastAPI Gateway
                      |
                Model Router
                      |
          +-----------+-----------+
          |                       |
       Primary                  Fallbacks
          |                       |
          +-----------+-----------+
                      |
              Provider Runtime
                      |
       +--------------+--------------+
       |              |              |
 OpenAI-compatible  Specialized   Local
     adapter          adapter     runtime
       |              |              |
     APIs          provider API  Ollama/LM Studio
```

The architecture deliberately separates wire protocols from routing and provider code. This mirrors the important architectural boundary in the current reference project: HTTP adapters, application routing/execution, provider runtime, CLI adapters and optional messaging are separate concerns. citeturn0search0

## Install

Python 3.10+.

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Start:

```bash
python -m my_free_code
```

Default address:

```text
http://127.0.0.1:8082
```

## Configure a model

Example:

```env
MODEL=open_router/openrouter/free
MODEL_SONNET=deepseek/deepseek-chat
MODEL_HAIKU=groq/llama-3.3-70b-versatile
MODEL_OPUS=nvidia_nim/meta/llama-3.3-70b-instruct
FALLBACK_MODELS=deepseek/deepseek-chat,ollama/llama3.1
```

Then set the corresponding API keys in `.env`.

The public model identity stays as the gateway model even when a request is routed to another upstream provider.

## Claude Code

```powershell
$env:ANTHROPIC_BASE_URL="http://127.0.0.1:8082"
$env:ANTHROPIC_AUTH_TOKEN="local"
$env:CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY="1"
claude
```

Or:

```bash
python -m my_free_code.cli.mfc claude
```

## Other clients

The launcher abstraction supports:

```bash
python -m my_free_code.cli.mfc codex
python -m my_free_code.cli.mfc pi
python -m my_free_code.cli.mfc opencode
python -m my_free_code.cli.mfc cline
python -m my_free_code.cli.mfc hermes
python -m my_free_code.cli.mfc deepseek-harness
python -m my_free_code.cli.mfc grok
python -m my_free_code.cli.mfc muse
```

The installed client must already exist on PATH.

## Routing and fallback

For:

```env
MODEL_SONNET=deepseek/deepseek-chat
FALLBACK_MODELS=groq/llama-3.3-70b-versatile,ollama/llama3.1
```

a Sonnet request follows:

```text
Claude Code
    |
    v
deepseek/deepseek-chat
    |
    | failure before output
    v
groq/llama-3.3-70b-versatile
    |
    | failure before output
    v
ollama/llama3.1
```

Once a streaming response has committed output, the gateway does not silently switch providers and duplicate the turn.

## Reasoning

The gateway accepts Claude-style thinking intent and keeps it separate from provider-specific request translation.

Supported normalized modes:

```text
auto
on
off
```

and optional effort:

```text
low
medium
high
```

Provider adapters can map the normalized reasoning policy to their documented upstream fields.

## Admin

Open:

```text
http://127.0.0.1:8082/admin
```

Authenticated JSON endpoints:

```text
GET /api/admin/status
GET /api/admin/models
GET /api/admin/providers
```

## Local models

Ollama:

```env
OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
MODEL=ollama/llama3.1
```

LM Studio:

```env
LM_STUDIO_BASE_URL=http://127.0.0.1:1234/v1
MODEL=lmstudio/qwen3.5-coder
```

llama.cpp:

```env
LLAMACPP_BASE_URL=http://127.0.0.1:8080/v1
MODEL=llamacpp/my-model
```

## Security

This is intended for local use.

- keep `HOST=127.0.0.1`
- set a non-trivial `PROXY_AUTH_TOKEN`
- never commit `.env`
- do not expose Admin endpoints directly to the Internet
- provider credentials remain in environment/configuration and are never sent to another provider

## Tests

```bash
pytest -q
```

The repository includes deterministic tests for routing, protocol conversion, auth, reasoning, model catalog and streaming primitives.

## Current scope vs. the reference

The current reference Free Claude Code has grown into a substantially larger product with a local proxy, many provider integrations, multiple coding agents, model catalog, recovery/fallback, local optimizations, desktop/IDE integrations and optional Discord/Telegram/voice workflows. citeturn0search1turn0search6

My Free Code v0.8 implements the **core of that architecture**, but it deliberately does not claim parity where an external client or provider requires proprietary SDK/authentication or a real external service. In particular:

- the provider catalog is broad, but only providers with a compatible transport or implemented adapter are immediately usable;
- launcher adapters prepare supported clients but do not install those clients;
- Discord/Telegram/voice are extension points, not bundled external-service implementations;
- provider-specific reasoning formats still need deeper adapter work for maximum fidelity;
- production deployment should add persistent state, metrics and stronger secret management.

That distinction is intentional: a catalog entry is metadata; a working integration is an adapter plus credentials plus a tested upstream contract.

## Project structure

```text
my-free-code/
├── my_free_code/
│   ├── api/
│   │   ├── routes.py
│   │   └── admin_routes.py
│   ├── cli/
│   │   ├── claude.py
│   │   ├── launchers.py
│   │   └── mfc.py
│   ├── core/
│   │   ├── anthropic.py
│   │   ├── responses.py
│   │   ├── reasoning.py
│   │   ├── failures.py
│   │   ├── streaming.py
│   │   └── model_catalog.py
│   └── providers/
│       ├── catalog.py
│       ├── adapters.py
│       ├── specialized.py
│       └── runtime.py
├── tests/
├── ARCHITECTURE.md
├── .env.example
├── requirements.txt
├── pyproject.toml
└── README.md
```

## License

MIT.
