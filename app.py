import datetime
import os

import flask
from flask import Flask

from src.blueprints.factory import factory
from src.blueprints.warehouse import warehouse

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.config['SESSION_COOKIE_SECURE'] = True
app.permanent_session_lifetime = datetime.timedelta(minutes=15)

app.register_blueprint(factory, url_prefix='/factory')
app.register_blueprint(warehouse, url_prefix='/warehouse')


@app.route('/')
def homepage() -> str:
    return flask.render_template('homepage/homepage.html')


@app.route('/factory')
def factory_redirect() -> flask.Response:
    return flask.redirect(flask.url_for('factory.login'))


@app.route('/details')
def details() -> str:
    return flask.render_template('homepage/details.html')


@app.route('/acknowledgements')
def acknowledgements() -> str:
    return flask.render_template('homepage/acknowledgements.html')


if __name__ == '__main__':
    app.run(debug=True)
