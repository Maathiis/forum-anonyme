from flask import Flask, request, redirect, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        requests.post('http://api:5000/messages', json={'username': username, 'message': message})
        return redirect('/')
    return render_template('form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
