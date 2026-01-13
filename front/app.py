import requests
from flask import Flask, redirect, render_template, request  # type: ignore

app = Flask(__name__)

API_BASE_URL = "http://api:5000"


@app.get("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        message = request.form.get("message", "").strip()

        if not username or not message:
            error = "Le pseudonyme et le message sont obligatoires."
        else:
            try:
                r = requests.post(
                    f"{API_BASE_URL}/messages",
                    json={"username": username, "message": message},
                    timeout=5,
                )
                r.raise_for_status()
                return redirect("/")
            except requests.exceptions.RequestException as e:
                error = f"Erreur lors de l’envoi du message : {e}"

    messages = []
    try:
        r = requests.get(f"{API_BASE_URL}/messages", timeout=5)
        r.raise_for_status()
        messages = r.json()
    except requests.exceptions.RequestException as e:
        error = error or f"Erreur lors de la récupération des messages : {e}"

    return render_template("index.html", messages=messages, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

