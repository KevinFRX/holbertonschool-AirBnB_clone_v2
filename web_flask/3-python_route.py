#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """comment"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """comment"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """comment"""
    text = text.replace("_", " ")
    return "C " + text


@app.route('/python')
@app.route('/python/<text>')
def python(text="is cool"):
    """comment"""
    text = text.replace("_", " ")
    return "Python {}".format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
