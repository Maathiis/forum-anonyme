from __future__ import annotations

from typing import Any

import pytest

from front.app import app


class _Resp:
    def __init__(self, status_code: int = 200, payload: Any | None = None):
        self.status_code = status_code
        self._payload = payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


@pytest.fixture()
def client():
    app.testing = True
    with app.test_client() as c:
        yield c


def test_get_index_renders_messages(monkeypatch, client):
    def fake_get(url: str, timeout: int = 5):
        assert url.endswith("/messages")
        return _Resp(200, [(1, "alice", "hello")])

    monkeypatch.setattr("front.app.requests.get", fake_get)

    r = client.get("/")
    assert r.status_code == 200
    html = r.data.decode("utf-8")
    assert "Forum Anonyme" in html
    assert "alice" in html
    assert "hello" in html


def test_post_index_requires_fields(monkeypatch, client):
    def empty_messages_get(*_a, **_k):
        return _Resp(200, [])

    monkeypatch.setattr("front.app.requests.get", empty_messages_get)

    r = client.post("/", data={"username": "", "message": ""})
    assert r.status_code == 200
    html = r.data.decode("utf-8")
    assert "obligatoires" in html


def test_post_index_sends_message_and_redirects(monkeypatch, client):
    def empty_messages_get(*_a, **_k):
        return _Resp(200, [])

    monkeypatch.setattr("front.app.requests.get", empty_messages_get)

    called = {"ok": False}

    def fake_post(url: str, json: Any, timeout: int = 5):
        assert url.endswith("/messages")
        assert json["username"] == "alice"
        assert json["message"] == "hello"
        called["ok"] = True
        return _Resp(200, {"message": "ok"})

    monkeypatch.setattr("front.app.requests.post", fake_post)

    r = client.post("/", data={"username": "alice", "message": "hello"})
    assert r.status_code == 302
    assert called["ok"] is True
