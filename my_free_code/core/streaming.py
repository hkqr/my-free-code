import json

def sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"

def openai_delta_to_anthropic(delta: dict, index: int = 0):
    events = []
    if delta.get("content"):
        events.append(sse("content_block_delta", {
            "type": "content_block_delta",
            "index": index,
            "delta": {"type": "text_delta", "text": delta["content"]},
        }))
    # Preserve provider reasoning when it is exposed in a common field.
    reasoning = delta.get("reasoning_content") or delta.get("reasoning")
    if reasoning:
        events.append(sse("content_block_delta", {
            "type": "content_block_delta",
            "index": index,
            "delta": {"type": "thinking_delta", "thinking": reasoning},
        }))
    return events
