import json


def test_chat_stream_mock(client):
    body = {"messages": [{"role": "user", "content": "Hi"}]}
    with client.stream("POST", "/api/chat/stream", json=body) as res:
        assert res.status_code == 200
        assert res.headers["content-type"].startswith("text/event-stream")
        events = [line[len("data: ") :] for line in res.iter_lines() if line.startswith("data: ")]

    assert events[-1] == "[DONE]"
    text = "".join(json.loads(e)["delta"] for e in events[:-1])
    assert "mock reply" in text
