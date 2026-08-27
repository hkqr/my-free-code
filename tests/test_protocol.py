from my_free_code.core.anthropic import anthropic_to_openai, openai_to_anthropic, rough_token_count

def test_anthropic_conversion():
    body = {
        "model": "sonnet",
        "system": "You are helpful",
        "messages": [{"role":"user","content":"hello"}],
        "max_tokens": 100,
    }
    out = anthropic_to_openai(body, "test-model")
    assert out["model"] == "test-model"
    assert out["messages"][0]["role"] == "system"
    assert out["messages"][1]["content"] == "hello"

def test_response_conversion():
    data = {
        "id": "x",
        "choices": [{"message":{"content":"hello"},"finish_reason":"stop"}],
        "usage":{"prompt_tokens":3,"completion_tokens":2},
    }
    out = openai_to_anthropic(data, "provider/test")
    assert out["content"][0]["text"] == "hello"
    assert out["usage"]["output_tokens"] == 2

def test_token_counter():
    assert rough_token_count({"messages":[{"role":"user","content":"hello"}]}) > 0
