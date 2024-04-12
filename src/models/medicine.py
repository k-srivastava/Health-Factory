"""Medicine model and related functions to query the database."""
import sqlite3
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional, Any


@dataclass(frozen=True, slots=True)
class Medicine:
    """Medicine model."""
    id: int
    name: str
    manufacturer_id: int
    cost_price: float
    sale_price: float
    potency: Optional[int]
    quantity_per_unit: int
    manufacturing_date: date
    purchase_date: date
    expiry_date: date

    @property
    def profit(self) -> float:
        """
        Calculate the profit per sale of the medicine.

        @return: Profit per sale of the medicine.
        @rtype: float
        """
        return self.sale_price - self.cost_price

    @property
    def time_to_expire(self) -> timedelta:
        """
        Calculate the time till the medicine expires from the current date.

        @return: Time till the medicine expires.
        @rtype: timedelta
        """
        return self.expiry_date - date.today()


def _create_medicine(raw_data: tuple) -> Medicine:
    """
    Create a medicine object from a record returned from the database.

    @param raw_data: Data returned from the database from the medicine table.
    @type raw_data: tuple

    @return: Medicine object from the database.
    @rtype: Medicine
    """
    return Medicine(
        id=raw_data[0],
        name=raw_data[1],
        manufacturer_id=raw_data[2],
        cost_price=float(raw_data[3]),
        sale_price=float(raw_data[4]),
        potency=None if raw_data[5] == '' else raw_data[5],
        quantity_per_unit=raw_data[6],
        manufacturing_date=date.fromisoformat(raw_data[7]),
        purchase_date=date.fromisoformat(raw_data[8]),
        expiry_date=date.fromisoformat(raw_data[9])
    )


def get_all_ids(connection: sqlite3.Connection) -> set[int]:
    """
    Get all the IDs of the medicines in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the IDs of the medicines in the database.
    @rtype: set[int]
    """
    cursor = connection.cursor()
    ids: list[tuple[int]] = cursor.execute('SELECT id FROM medicine').fetchall()
    cursor.close()

    return {id_[0] for id_ in ids}


def get_by_id(connection: sqlite3.Connection, medicine_id: int) -> Optional[Medicine]:
    """
    Get the medicine by its unique ID.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection
    @param medicine_id: Medicine ID.
    @type medicine_id: int

    @return: Medicine in the database, or None if the customer does not exist.
    @rtype: Optional[Medicine]
    """
    cursor = connection.cursor()
    medicine_raw = cursor.execute('SELECT * FROM medicine WHERE id = ?', (medicine_id,)).fetchone()
    cursor.close()

    if medicine_raw is None:
        return None

    return _create_medicine(medicine_raw)


def get_all(connection: sqlite3.Connection) -> set[Medicine]:
    """
    Get all the medicines in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the medicines in the database.
    @rtype: set[Medicine]
    """
    medicines = set()

    cursor = connection.cursor()
    medicines_raw = cursor.execute('SELECT * FROM medicine').fetchall()
    cursor.close()

    for medicine in medicines_raw:
        medicines.add(_create_medicine(medicine))

    return medicines


def get_all_with_fields(connection: sqlite3.Connection, *fields: str) -> list[dict[str, Any]]:
    data = []
    column_names = ', '.join(fields)

    cursor = connection.cursor()
    medicines_raw = cursor.execute(f'SELECT {column_names} FROM medicine').fetchall()
    cursor.close()

    for medicine in medicines_raw:
        dictionary = dict()

        for idx, field in enumerate(fields):
            dictionary[field] = medicine[idx]

        data.append(dictionary)

    return data


def insert(connection: sqlite3.Connection, medicine: Medicine):
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO medicine VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (
            medicine.id, medicine.name, medicine.manufacturer_id, medicine.cost_price, medicine.sale_price,
            medicine.potency, medicine.quantity_per_unit, medicine.manufacturing_date, medicine.purchase_date,
            medicine.expiry_date
        )
    )
    cursor.close()


def update(connection: sqlite3.Connection, medicine: Medicine):
    cursor = connection.cursor()
    cursor.execute(
        '''UPDATE medicine
        SET name = ?, manufacturer_id = ?, cost_price = ?, sale_price = ?, potency = ?, quantity_per_unit = ?, 
        manufacturing_date = ?, purchase_date = ?, expiry_date = ? WHERE id = ?''',
        (
            medicine.name, medicine.manufacturer_id, medicine.cost_price, medicine.sale_price, medicine.potency,
            medicine.quantity_per_unit, medicine.manufacturing_date, medicine.purchase_date, medicine.expiry_date,
            medicine.id
        )
    )
    cursor.close()
