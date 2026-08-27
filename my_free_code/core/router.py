from ..config import Settings

def select_model(requested: str | None, s: Settings) -> str:
    value = (requested or "").lower()
    if "/" in value:
        return requested or s.model
    if "opus" in value and s.opus:
        return s.opus
    if "sonnet" in value and s.sonnet:
        return s.sonnet
    if "haiku" in value and s.haiku:
        return s.haiku
    if "fable" in value and s.fable:
        return s.fable
    return s.model

def candidates(primary: str, s: Settings) -> list[str]:
    return list(dict.fromkeys([primary, *s.fallbacks]))

def split_model(model: str) -> tuple[str, str]:
    provider, sep, remote = model.partition("/")
    if not sep or not provider or not remote:
        raise ValueError("model must have the form provider/model")
    return provider, remote
