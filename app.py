import os

import flask
from flask import Flask

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')


@app.route('/')
def homepage() -> str:
    return flask.render_template('homepage/homepage.html')


@app.route('/details')
def details() -> str:
    return flask.render_template('homepage/details.html')


@app.route('/acknowledgements')
def acknowledgements() -> str:
    return flask.render_template('homepage/acknowledgements.html')


if __name__ == '__main__':
    app.run()
