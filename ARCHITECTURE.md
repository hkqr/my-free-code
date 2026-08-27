# My Free Code v0.8 Architecture

## Goal

Provide a stable local gateway for coding agents while keeping provider-specific behavior behind adapters.

## Boundaries

- `api/`: HTTP wire contracts and admin endpoints.
- `core/`: protocol-neutral routing helpers, Anthropic/OpenAI conversion, reasoning policy, SSE primitives, failure semantics and model catalog.
- `providers/`: provider metadata, generic transport, specialized profiles, concurrency/rate limiting and recovery state.
- `cli/`: local launchers for coding-agent processes.
- `tests/`: deterministic contract tests.

## Request lifecycle

```text
Client
  |
  v
API route
  |
  v
ModelRouter
  |
  +--> public gateway model
  |
  +--> provider/model target
  |
  v
ProviderRuntime
  |
  +--> admission control
  +--> adapter selection
  +--> upstream request
  +--> stream normalization
  |
  v
wire response
```

## Routing invariant

The public model and upstream model are different identities.

Example:

```text
public:  claude-sonnet
upstream: deepseek/deepseek-chat
```

The upstream provider must never replace the public identity in the response.

## Fallback invariant

A fallback can be selected only before the current candidate has committed observable output. This prevents duplicated partial answers.

```text
primary
  |
  +-- pre-commit failure --> fallback
  |
  +-- committed output --> terminal result
```

## Provider adapters

`ProviderAdapter` is the extension point.

The shared OpenAI Chat adapter handles providers exposing:

```text
POST /chat/completions
```

Specialized profiles exist for major provider families. They currently inherit the common transport where the wire contract is compatible; they can override request, authentication and stream handling without changing the gateway.

## Reasoning

Reasoning is resolved once at the gateway boundary:

```text
client intent
    |
    v
ReasoningPolicy
    |
    +--> provider adapter
```

This avoids branching on provider model names throughout the application.

## Model catalog

The catalog contains:

1. gateway compatibility IDs;
2. configured provider/model IDs;
3. fallback IDs.

`/v1/models` exposes the resulting inventory.

## Client launchers

Every launcher follows the same principle:

```text
installed client
      |
      v
local proxy environment
      |
      v
client process
```

The launcher does not bypass the provider's own authentication or pretend to be an official provider client.

## Future extension points

- provider-specific reasoning codecs;
- native OpenAI Responses upstream adapters;
- persistent provider health/circuit state;
- metrics and tracing;
- real Codex model catalog file generation;
- Discord/Telegram managed sessions;
- voice transcription adapters;
- RTK-style terminal-output reduction.
