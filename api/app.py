import os

from flask import Flask, jsonify, request  # type: ignore

app = Flask(__name__)


def _get_secret_value(env_name: str, default: str) -> str:
    """
    Permet d'utiliser des secrets Swarm/K8s via *_FILE (ex: DB_PASSWORD_FILE).
    """
    file_path = os.getenv(f"{env_name}_FILE")
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except OSError:
            pass
    return os.getenv(env_name, default)


DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "forum")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = _get_secret_value("DB_PASSWORD", "password")


def get_db_connection():
    try:
        import psycopg2  # type: ignore
    except ModuleNotFoundError as e:  # pragma: no cover
        raise RuntimeError(
            "psycopg2 n'est pas installé. Installe les dépendances API "
            "(`pip install -r api/requirements.txt`)."
        ) from e

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    return conn


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/messages", methods=["GET"])
def get_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages;")
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(messages)


@app.route("/messages", methods=["POST"])
def add_message():
    data = request.get_json()
    username = data["username"]
    message = data["message"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (username, message) VALUES (%s, %s)",
        (username, message),
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Message added successfully!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
