import os
import sqlite3

import flask
import werkzeug.security as security

from src.models import employee

factory = flask.Blueprint('factory', __name__)


@factory.route('/login', methods=['POST', 'GET'])
def login() -> flask.Response | str:
    login_message = ''

    if flask.request.method == 'POST':
        email_address = flask.request.form['email-address']
        password = flask.request.form['password']

        connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
        login_employee = employee.get_by_email_address(connection, email_address)
        connection.close()

        if login_employee is not None and security.check_password_hash(login_employee.login_password, password):
            flask.session['employee_id'] = login_employee.id
            flask.session.permanent = True

            return flask.redirect(flask.url_for('factory.dashboard'))

        login_message = 'Invalid email or password.'

    return flask.render_template('factory/login.html', login_message=login_message)


@factory.route('/logout')
def logout() -> flask.Response:
    flask.session.pop('employee_id', None)
    return flask.redirect(flask.url_for('factory.login'))


@factory.route('/dashboard')
def dashboard() -> flask.Response | str:
    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    employee_name = employee.get_by_id(connection, flask.session.get('employee_id'))
    connection.close()

    return f'<h1>{employee_name}</h1>'
