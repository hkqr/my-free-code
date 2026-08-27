import json

def content_text(value):
    if isinstance(value, str):
        return value
    return "\n".join(
        str(x.get("text", "")) for x in value
        if isinstance(x, dict) and x.get("type") == "text"
    )

def anthropic_to_openai(body: dict, remote_model: str) -> dict:
    messages = []
    system = body.get("system")
    if system:
        messages.append({"role": "system", "content": content_text(system)})

    for msg in body.get("messages", []):
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if isinstance(content, str):
            messages.append({"role": role, "content": content})
            continue

        parts = []
        tool_calls = []
        for block in content:
            kind = block.get("type")
            if kind == "text":
                parts.append({"type": "text", "text": block.get("text", "")})
            elif kind == "image":
                src = block.get("source", {})
                if src.get("type") == "base64":
                    parts.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{src.get('media_type','image/png')};base64,{src.get('data','')}"
                        }
                    })
            elif kind == "tool_use":
                tool_calls.append({
                    "id": block.get("id"),
                    "type": "function",
                    "function": {
                        "name": block.get("name"),
                        "arguments": json.dumps(block.get("input", {}))
                    }
                })
            elif kind == "tool_result":
                messages.append({
                    "role": "tool",
                    "tool_call_id": block.get("tool_use_id"),
                    "content": content_text(block.get("content", ""))
                })

        item = {"role": role, "content": parts}
        if tool_calls:
            item["tool_calls"] = tool_calls
        messages.append(item)

    out = {
        "model": remote_model,
        "messages": messages,
        "stream": bool(body.get("stream")),
        "max_tokens": body.get("max_tokens", 4096),
    }
    for key in ("temperature", "top_p", "stop"):
        if key in body:
            out[key] = body[key]

    if body.get("tools"):
        out["tools"] = [{
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t.get("description", ""),
                "parameters": t.get("input_schema", {}),
            }
        } for t in body["tools"]]

    if body.get("tool_choice"):
        out["tool_choice"] = body["tool_choice"]

    return out

def openai_to_anthropic(data: dict, requested_model: str) -> dict:
    choice = (data.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    blocks = []

    if message.get("content"):
        blocks.append({"type": "text", "text": message["content"]})

    for call in message.get("tool_calls") or []:
        fn = call.get("function") or {}
        raw = fn.get("arguments", "{}")
        try:
            args = json.loads(raw)
        except (ValueError, TypeError):
            args = {"raw": raw}
        blocks.append({
            "type": "tool_use",
            "id": call.get("id"),
            "name": fn.get("name"),
            "input": args,
        })

    reason = {
        "stop": "end_turn",
        "length": "max_tokens",
        "tool_calls": "tool_use",
    }.get(choice.get("finish_reason"), "end_turn")

    usage = data.get("usage") or {}
    return {
        "id": data.get("id", "msg_proxy"),
        "type": "message",
        "role": "assistant",
        "model": requested_model,
        "content": blocks or [{"type": "text", "text": ""}],
        "stop_reason": reason,
        "stop_sequence": None,
        "usage": {
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
        },
    }

def rough_token_count(body: dict) -> int:
    return max(1, len(json.dumps(body, ensure_ascii=False)) // 4)
