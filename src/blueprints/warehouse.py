import datetime
import json
import os
import sqlite3

import flask

from src.models import customer as customer_model
from src.models import employee as employee_model
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


@warehouse.route('/manufacturers/update', methods=['GET', 'POST'])
def manufacturer_update() -> flask.Response | str:
    submission_message = ''

    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    current_user_data = employee_model.get_by_id(connection, flask.session.get('employee_id'))
    manufacturer_ids = manufacturer_model.get_all_ids(connection)
    connection.close()

    if not current_user_data.is_administrator:
        return flask.redirect(flask.url_for('factory.login'))

    if flask.request.method == 'POST':
        form_output = flask.request.form

        id_ = int(form_output.get('manufacturer-id'))
        name = form_output.get('manufacturer-name')
        phone_number = form_output.get('manufacturer-phone-number')
        address = form_output.get('manufacturer-address')

        manufacturer_instance = manufacturer_model.Manufacturer(id_, name, phone_number, address)

        connection = sqlite3.connect(os.getenv('DATABASE_PATH'))

        if id_ not in manufacturer_ids:
            manufacturer_model.insert(connection, manufacturer_instance)
            submission_message = 'Manufacturer created.'
        else:
            manufacturer_model.update(connection, manufacturer_instance)
            submission_message = 'Manufacturer updated.'

        connection.commit()
        connection.close()

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))

    manufacturers_all = manufacturer_model.get_all(connection)
    manufacturer_data = manufacturer_model.get_all_with_fields(connection, 'id', 'name', 'phone_number', 'address')
    connection.close()

    encoder = json.JSONEncoder()
    manufacturer_json = encoder.encode(manufacturer_data)

    return flask.render_template(
        'warehouse/manufacturer_update.html', model_name='manufacturer', models=manufacturers_all,
        model_json=manufacturer_json, model_ids=manufacturer_ids, submission_message=submission_message
    )


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


@warehouse.route('/medicines/update', methods=['GET', 'POST'])
def medicine_update() -> flask.Response | str:
    submission_message = ''

    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    current_user_data = employee_model.get_by_id(connection, flask.session.get('employee_id'))
    medicine_ids = medicine_model.get_all_ids(connection)
    connection.close()

    if not current_user_data.is_administrator:
        return flask.redirect(flask.url_for('factory.login'))

    if flask.request.method == 'POST':
        form_output = flask.request.form

        id_ = int(form_output.get('medicine-id'))
        name = form_output.get('medicine-name')
        manufacturer_id = int(form_output.get('medicine-manufacturer-id'))
        cost_price = float(form_output.get('medicine-cost-price'))
        sale_price = float(form_output.get('medicine-sale-price'))
        potency = int(form_output.get('medicine-potency')) if form_output.get('medicine-potency') != '' else None
        quantity_per_unit = int(form_output.get('medicine-quantity-per-unit'))
        manufacturing_date = datetime.date.fromisoformat(form_output.get('medicine-manufacturing-date'))
        purchase_date = datetime.date.fromisoformat(form_output.get('medicine-purchase-date'))
        expiry_date = datetime.date.fromisoformat(form_output.get('medicine-expiry-date'))

        medicine_instance = medicine_model.Medicine(
            id_, name, manufacturer_id, cost_price, sale_price, potency,
            quantity_per_unit, manufacturing_date, purchase_date, expiry_date
        )

        connection = sqlite3.connect(os.getenv('DATABASE_PATH'))

        if id_ not in medicine_ids:
            medicine_model.insert(connection, medicine_instance)
            submission_message = 'Medicine created.'
        else:
            medicine_model.update(connection, medicine_instance)
            submission_message = 'Medicine updated.'

        connection.commit()
        connection.close()

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))

    medicines_all = medicine_model.get_all(connection)
    medicine_data = medicine_model.get_all_with_fields(
        connection, 'id', 'name', 'manufacturer_id', 'cost_price', 'sale_price', 'potency', 'quantity_per_unit',
        'manufacturing_date', 'purchase_date', 'expiry_date'
    )
    manufacturer_ids = manufacturer_model.get_all_ids(connection)

    encoder = json.JSONEncoder()
    medicine_json = encoder.encode(medicine_data)

    return flask.render_template(
        'warehouse/medicine_update.html', model_name='medicine', models=medicines_all,
        model_json=medicine_json, model_ids=medicine_ids, manufacturer_ids=manufacturer_ids,
        submission_message=submission_message
    )


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


@warehouse.route('/sales/update', methods=['GET', 'POST'])
def sale_update() -> flask.Response | str:
    submission_message = ''

    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    current_user_data = employee_model.get_by_id(connection, flask.session.get('employee_id'))
    sale_ids = sale_model.get_all_ids(connection)
    connection.close()

    if not current_user_data.is_administrator:
        return flask.redirect(flask.url_for('factory.login'))

    if flask.request.method == 'POST':
        form_output = flask.request.form

        id_ = int(form_output.get('sale-id'))
        date_time = datetime.datetime.fromisoformat(form_output.get('sale-date-time'))
        employee_id = int(form_output.get('sale-employee-id'))
        customer_id = int(form_output.get('sale-customer-id'))
        amount = float(form_output.get('sale-amount'))

        sale_instance = sale_model.Sale(id_, date_time, employee_id, customer_id, amount)

        connection = sqlite3.connect(os.getenv('DATABASE_PATH'))

        if id_ not in sale_ids:
            sale_model.insert(connection, sale_instance)
            submission_message = 'Sale created.'
        else:
            sale_model.update(connection, sale_instance)
            submission_message = 'Sale updated.'

        connection.commit()
        connection.close()

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))

    sales_all = sale_model.get_all(connection)
    sale_data = sale_model.get_all_with_fields(connection, 'id', 'date_time', 'employee_id', 'customer_id', 'amount')

    employee_ids = employee_model.get_all_ids(connection)
    customer_ids = customer_model.get_all_ids(connection)

    encoder = json.JSONEncoder()
    sale_json = encoder.encode(sale_data)

    return flask.render_template(
        'warehouse/sale_update.html', model_name='sale', models=sales_all, model_json=sale_json,
        model_ids=sale_ids, employee_ids=employee_ids, customer_ids=customer_ids, submission_message=submission_message
    )


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


@warehouse.route('/salts/update', methods=['GET', 'POST'])
def salt_update() -> flask.Response | str:
    submission_message = ''

    if 'employee_id' not in flask.session:
        return flask.redirect(flask.url_for('factory.login'))

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))
    current_user_data = employee_model.get_by_id(connection, flask.session.get('employee_id'))
    salt_ids = salt_model.get_all_ids(connection)
    connection.close()

    if not current_user_data.is_administrator:
        return flask.redirect(flask.url_for('factory.login'))

    if flask.request.method == 'POST':
        form_output = flask.request.form

        id_ = int(form_output.get('salt-id'))
        name = form_output.get('salt-name')

        salt_instance = salt_model.Salt(id_, name)

        connection = sqlite3.connect(os.getenv('DATABASE_PATH'))

        if id_ not in salt_ids:
            salt_model.insert(connection, salt_instance)
            submission_message = 'Salt created.'
        else:
            salt_model.update(connection, salt_instance)
            submission_message = 'Salt updated.'

        connection.commit()
        connection.close()

    connection = sqlite3.connect(os.getenv('DATABASE_PATH'))

    salts_all = salt_model.get_all(connection)
    salt_data = salt_model.get_all_with_fields(connection, 'id', 'name')

    encoder = json.JSONEncoder()
    salt_json = encoder.encode(salt_data)

    return flask.render_template(
        'warehouse/salt_update.html', model_name='salt', models=salts_all, model_json=salt_json,
        submission_message=submission_message
    )
