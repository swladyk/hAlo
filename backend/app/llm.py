"""The ONLY place that calls an LLM provider. Empty LLM_API_KEY = mock mode."""

import asyncio
from collections.abc import AsyncIterator

from app.config import settings

DEFAULT_MODEL = "gpt-4o-mini"
MOCK_REPLY = (
    "This is a mock reply from hAlo. Set LLM_API_KEY in backend/.env to talk to a real model."
)


def is_live() -> bool:
    return bool(settings.llm_api_key)


async def stream_chat(messages: list[dict]) -> AsyncIterator[str]:
    """Yield the assistant reply as text chunks. messages: [{"role": ..., "content": ...}]."""
    if not is_live():
        for i, word in enumerate(MOCK_REPLY.split(" ")):
            yield word if i == 0 else " " + word
            await asyncio.sleep(0.03)
        return

    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.llm_api_key)
    stream = await client.chat.completions.create(
        model=settings.llm_model or DEFAULT_MODEL,
        messages=messages,
        stream=True,
    )
    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
