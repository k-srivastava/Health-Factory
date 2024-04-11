import json
import os
import sqlite3

import flask

from src.models import manufacturer as manufacturer_model
from src.models import medicine as medicine_model
from src.models import sale as sale_model
from src.models import salt as salt_model

warehouse = flask.Blueprint('warehouse', __name__)


@warehouse.route('/')
def home() -> flask.Response | str:
    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    return flask.render_template('warehouse/home.html')


@warehouse.route('/manufacturers')
def manufacturers() -> flask.Response | str:
    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    manufacturer_data = manufacturer_model.get_all_with_fields(connection, 'id', 'name', 'phone_number')
    connection.close()

    encoder = json.JSONEncoder()
    manufacturer_json = encoder.encode(manufacturer_data)

    return flask.render_template('warehouse/manufacturers.html', manufacturers=manufacturer_json)


@warehouse.route('/manufacturers/<int:manufacturer_id>')
def manufacturer(manufacturer_id: int) -> flask.Response | str:
    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    manufacturer_data = manufacturer_model.get_by_id(connection, manufacturer_id)
    connection.close()

    if manufacturer_data is None:
        return flask.redirect(flask.url_for('warehouse.home'))

    return flask.render_template('warehouse/manufacturer_view.html', manufacturer=manufacturer_data)


@warehouse.route('/medicines')
def medicines() -> flask.Response | str:
    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    medicine_data = medicine_model.get_all_with_fields(connection, 'id', 'name')
    connection.close()

    encoder = json.JSONEncoder()
    medicine_json = encoder.encode(medicine_data)

    return flask.render_template('warehouse/medicines.html', medicines=medicine_json)


@warehouse.route('/medicines/<int:medicine_id>')
def medicine(medicine_id: int) -> flask.Response | str:
    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    medicine_data = medicine_model.get_by_id(connection, medicine_id)
    connection.close()

    if medicine_data is None:
        return flask.redirect(flask.url_for('warehouse.home'))

    return flask.render_template('warehouse/medicine_view.html', medicine=medicine_data)


@warehouse.route('/sales')
def sales() -> flask.Response | str:
    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    sale_data = sale_model.get_all_with_fields(connection, 'id', 'date_time')
    connection.close()

    encoder = json.JSONEncoder()
    sale_json = encoder.encode(sale_data)

    return flask.render_template('warehouse/sales.html', sales=sale_json)


@warehouse.route('/sales/<int:sale_id>')
def sale(sale_id: int) -> flask.Response | str:
    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    sale_data = sale_model.get_by_id(connection, sale_id)
    connection.close()

    if sale_data is None:
        return flask.redirect(flask.url_for('warehouse.home'))

    return flask.render_template('warehouse/sale_view.html', sale=sale_data)


@warehouse.route('/salts')
def salts() -> flask.Response | str:
    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    salt_data = salt_model.get_all_with_fields(connection, 'id', 'name')
    connection.close()

    encoder = json.JSONEncoder()
    salt_json = encoder.encode(salt_data)

    return flask.render_template('warehouse/salts.html', salts=salt_json)


@warehouse.route('/salts/<int:salt_id>')
def salt(salt_id: int) -> flask.Response | str:
    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    salt_data = salt_model.get_by_id(connection, salt_id)
    connection.close()

    if salt_data is None:
        return flask.redirect(flask.url_for('warehouse.home'))

    return flask.render_template('warehouse/salt_view.html', salt=salt_data)
