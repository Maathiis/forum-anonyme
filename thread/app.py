from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    try:
        response = requests.get('http://api:5000/messages')
        response.raise_for_status()  # Raise an error for bad status codes
        messages = response.json()
        return render_template('index.html', messages=messages)
    except requests.exceptions.RequestException as e:
        return f"Error fetching messages: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
