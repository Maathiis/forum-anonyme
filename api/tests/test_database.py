from __future__ import annotations

import os
import time

import pytest


@pytest.mark.integration
def test_database_roundtrip():
    """
    Test d'intégration (optionnel) qui vérifie un aller-retour DB.
    À lancer quand une DB de test est disponible (ex: docker compose up db).
    """
    host = os.getenv("DB_HOST", "")
    if not host:
        pytest.skip("DB_HOST non défini (test d’intégration DB ignoré)")

    dbname = os.getenv("DB_NAME", "forum")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "password")

    try:
        import psycopg2  # type: ignore
    except ModuleNotFoundError:
        pytest.skip("psycopg2 non installé (test d’intégration DB ignoré)")

    # Attente courte pour laisser Postgres démarrer si besoin
    deadline = time.time() + 10
    last_err: Exception | None = None
    conn = None
    while time.time() < deadline:
        try:
            conn = psycopg2.connect(
                host=host,
                database=dbname,
                user=user,
                password=password,
            )
            break
        except Exception as e:  # pragma: no cover
            last_err = e
            time.sleep(0.5)

    if conn is None:
        pytest.skip(f"DB inaccessible (dernier erreur: {last_err})")

    try:
        cur = conn.cursor()
        username = "pytest"
        message = f"hello-{int(time.time())}"

        cur.execute(
            "INSERT INTO messages (username, message) VALUES (%s, %s) RETURNING id",
            (username, message),
        )
        msg_id = cur.fetchone()[0]
        conn.commit()

        cur.execute("SELECT username, message FROM messages WHERE id = %s", (msg_id,))
        row = cur.fetchone()
        assert row == (username, message)

        cur.execute("DELETE FROM messages WHERE id = %s", (msg_id,))
        conn.commit()
        cur.close()
    finally:
        conn.close()

