from dataclasses import dataclass

@dataclass(frozen=True)
class ReasoningPolicy:
    mode: str = "auto"          # auto | on | off
    effort: str | None = None   # low | medium | high
    budget_tokens: int | None = None

def resolve_reasoning(request: dict, configured: str = "auto") -> ReasoningPolicy:
    thinking = request.get("thinking")
    if thinking == {"type": "disabled"}:
        return ReasoningPolicy("off")
    if isinstance(thinking, dict) and thinking.get("type") in {"enabled", "adaptive"}:
        budget = thinking.get("budget_tokens")
        return ReasoningPolicy("on", thinking.get("effort"), budget)
    return ReasoningPolicy(configured)
