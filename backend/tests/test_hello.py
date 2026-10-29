def test_create_and_list_messages(client):
    assert client.get("/api/hello/messages").json() == []

    for text in ["first", "second"]:
        res = client.post("/api/hello/messages", json={"text": text})
        assert res.status_code == 201
        assert res.json()["text"] == text

    texts = [m["text"] for m in client.get("/api/hello/messages").json()]
    assert texts == ["second", "first"]  # newest first


def test_empty_message_rejected(client):
    assert client.post("/api/hello/messages", json={"text": ""}).status_code == 422
