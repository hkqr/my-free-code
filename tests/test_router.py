from my_free_code.core.router import select_model, candidates
from my_free_code.config import Settings

def test_model_routing():
    s = Settings(model="open_router/free", sonnet="deepseek/deepseek-chat")
    assert select_model("sonnet", s) == "deepseek/deepseek-chat"

def test_explicit_model():
    s = Settings(model="open_router/free")
    assert select_model("groq/foo", s) == "groq/foo"

def test_fallbacks_are_unique():
    s = Settings(model="a/b", fallbacks=["c/d","a/b","c/d"])
    assert candidates("a/b", s) == ["a/b","c/d"]
