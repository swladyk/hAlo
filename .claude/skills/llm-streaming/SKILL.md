---
name: llm-streaming
description: How hAlo calls the LLM and streams results — app/llm.py, SSE event format, agent loops, and reading the stream in React. Use for any feature that uses an LLM, agent steps or streaming responses.
---

# LLM + streaming

## Backend
- **Only** call the model through `app/llm.py`: `async for delta in llm.stream_chat(messages)` where `messages = [{"role": "system"|"user"|"assistant", "content": str}]`. Never import `openai` in a feature.
- Provider is OpenAI (`AsyncOpenAI`, `LLM_MODEL`, default `gpt-4o-mini`). Need a new capability (e.g. non-streaming call, JSON output, tools)? Add a small function to `llm.py` **with a mock-mode branch** — it's a shared change, announce it.
- `LLM_API_KEY` empty → mock mode (fake word-by-word reply). Tests and CI always run in mock mode; never require a key.
- SSE format (see `app/features/chat/service.py`): each event is `data: <json>\n\n`; text chunks are `{"delta": "..."}`, errors `{"error": "..."}`, end is `data: [DONE]`. Custom events for agent steps: add a field, e.g. `{"step": {"tool": "...", "status": "..."}}` — keep `delta`/`[DONE]` semantics.
- Return `StreamingResponse(gen(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})`.
- Agent loops: hard `MAX_STEPS` constant (e.g. 8), break on it and emit a final event. No unbounded `while True`.

## Frontend
Use `streamSSE(path, body, onEvent)` from `@/lib/api` — it POSTs JSON and calls `onEvent` for each parsed `data:` JSON payload until `[DONE]`. Append `event.delta` to state as it arrives (see `src/features/chat/ChatBox.tsx`). Never call an LLM provider from the browser.

## Testing
```python
with client.stream("POST", "/api/<f>/stream", json=body) as res:
    events = [l[6:] for l in res.iter_lines() if l.startswith("data: ")]
assert events[-1] == "[DONE]"
```
