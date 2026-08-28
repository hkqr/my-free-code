from my_free_code.core.reasoning import resolve_reasoning
from my_free_code.core.model_catalog import public_catalog 
from my_free_code.core.streaming import openai_delta_to_anthropic
from my_free_code.config import Settings

def test_reasoning_disabled():
    p = resolve_reasoning({"thinking":{"type":"disabled"}})
    assert p.mode == "off"

def test_reasoning_budget():
    p = resolve_reasoning({"thinking":{"type":"enabled","budget_tokens":1234}})
    assert p.budget_tokens == 1234

def test_catalog_has_gateway_models():
    data = public_catalog(Settings(model="x/y"))
    assert "claude-sonnet" in data
    assert "x/y" in data

def test_stream_delta():
    events = openai_delta_to_anthropic({"content":"hi"})
    assert "text_delta" in events[0]
