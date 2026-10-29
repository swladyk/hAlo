import json
from collections.abc import AsyncIterator

from app import llm


def sse(data: str) -> str:
    return f"data: {data}\n\n"


async def stream_reply_sse(messages: list[dict]) -> AsyncIterator[str]:
    """Wrap llm.stream_chat as SSE events: data: {"delta": "..."} ... data: [DONE]."""
    try:
        async for delta in llm.stream_chat(messages):
            yield sse(json.dumps({"delta": delta}))
    except Exception as exc:
        yield sse(json.dumps({"error": str(exc)}))
    yield sse("[DONE]")
