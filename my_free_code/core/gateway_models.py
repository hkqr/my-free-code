from dataclasses import dataclass

GATEWAY_MODELS = {
    "claude-opus": "opus",
    "claude-sonnet": "sonnet",
    "claude-haiku": "haiku",
    "claude-fable": "fable",
    "claude-opus-no-thinking": "opus",
    "claude-sonnet-no-thinking": "sonnet",
    "claude-haiku-no-thinking": "haiku",
}

@dataclass(frozen=True)
class GatewayModel:
    id: str
    tier: str
    thinking: bool = True
