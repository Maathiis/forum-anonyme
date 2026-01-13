from __future__ import annotations

from typing import Any

import pytest

from api.app import app


class _FakeCursor:
    def __init__(self, rows: list[tuple[Any, ...]]):
        self._rows = rows
        self.queries: list[tuple[str, tuple[Any, ...] | None]] = []

    def execute(self, query: str, params: tuple[Any, ...] | None = None) -> None:
        self.queries.append((query, params))

    def fetchall(self) -> list[tuple[Any, ...]]:
        return self._rows

    def close(self) -> None:
        return None


class _FakeConn:
    def __init__(self, rows: list[tuple[Any, ...]]):
        self._rows = rows
        self.closed = False
        self.committed = False
        self.cursor_obj = _FakeCursor(rows)

    def cursor(self) -> _FakeCursor:
        return self.cursor_obj

    def commit(self) -> None:
        self.committed = True

    def close(self) -> None:
        self.closed = True


@pytest.fixture()
def client():
    app.testing = True
    with app.test_client() as c:
        yield c


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_get_messages_returns_rows(monkeypatch, client):
    fake_rows = [(1, "alice", "hello"), (2, "bob", "yo")]
    fake_conn = _FakeConn(fake_rows)

    monkeypatch.setattr("api.app.get_db_connection", lambda: fake_conn)

    r = client.get("/messages")
    assert r.status_code == 200
    # jsonify() convertit les tuples en listes
    assert r.get_json() == [list(row) for row in fake_rows]
    assert any("SELECT" in q[0] for q in fake_conn.cursor_obj.queries)


def test_post_messages_inserts(monkeypatch, client):
    fake_rows = []
    fake_conn = _FakeConn(fake_rows)

    monkeypatch.setattr("api.app.get_db_connection", lambda: fake_conn)

    r = client.post("/messages", json={"username": "alice", "message": "hello"})
    assert r.status_code == 200
    assert r.get_json() == {"message": "Message added successfully!"}
    assert fake_conn.committed is True
    assert any("INSERT INTO messages" in q[0] for q in fake_conn.cursor_obj.queries)

