def responses_to_messages(body: dict) -> dict:
    # Minimal normalization for Responses clients. Rich response items are
    # intentionally preserved as text/tool content rather than discarded.
    input_value = body.get("input", "")
    messages = []
    if isinstance(input_value, str):
        messages.append({"role": "user", "content": input_value})
    elif isinstance(input_value, list):
        for item in input_value:
            if isinstance(item, dict):
                role = item.get("role", "user")
                content = item.get("content", "")
                messages.append({"role": role, "content": content})
            else:
                messages.append({"role": "user", "content": str(item)})

    return {
        "messages": messages,
        "model": body.get("model", ""),
        "max_tokens": body.get("max_output_tokens", 4096),
        "stream": bool(body.get("stream")),
    }

def messages_to_response(message: dict) -> dict:
    text = "".join(
        b.get("text", "")
        for b in message.get("content", [])
        if isinstance(b, dict) and b.get("type") == "text"
    )
    return {
        "id": message.get("id"),
        "object": "response",
        "status": "completed",
        "model": message.get("model"),
        "output": [{
            "type": "message",
            "role": "assistant",
            "content": [{"type": "output_text", "text": text}],
        }],
        "usage": {
            "input_tokens": message.get("usage", {}).get("input_tokens", 0),
            "output_tokens": message.get("usage", {}).get("output_tokens", 0),
            "total_tokens": (
                message.get("usage", {}).get("input_tokens", 0)
                + message.get("usage", {}).get("output_tokens", 0)
            ),
        },
    }
