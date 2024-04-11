"""Manufacturer model and related functions to query the database."""
import sqlite3
from dataclasses import dataclass
from typing import Optional, Any


@dataclass(frozen=True, slots=True)
class Manufacturer:
    """Manufacturer model."""
    id: int
    name: str
    phone_number: str
    address: Optional[str]


def _create_manufacturer(raw_data: tuple) -> Manufacturer:
    """
    Create a manufacturer object from a record returned from the database.

    @param raw_data: Data returned from the database from the manufacturer table.
    @type raw_data: tuple

    @return: Manufacturer object from the database.
    @rtype: Manufacturer
    """
    return Manufacturer(
        id=raw_data[0],
        name=raw_data[1],
        phone_number=raw_data[2],
        address=None if raw_data[3] == '' else raw_data[3]
    )


def get_all_ids(connection: sqlite3.Connection) -> set[int]:
    """
    Get all the IDs of the manufacturers in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the IDs of the manufacturers in the database.
    @rtype: set[int]
    """
    cursor = connection.cursor()
    ids: list[tuple[int]] = cursor.execute('SELECT id FROM manufacturer').fetchall()
    cursor.close()

    return {id_[0] for id_ in ids}


def get_by_id(connection: sqlite3.Connection, manufacturer_id: int) -> Optional[Manufacturer]:
    """
    Get the manufacturer by its unique ID.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection
    @param manufacturer_id: Manufacturer ID.
    @type manufacturer_id: int

    @return: Manufacturer in the database, or None if the manufacturer does not exist.
    @rtype: Optional[Manufacturer]
    """
    cursor = connection.cursor()
    manufacturer_raw = cursor.execute('SELECT * FROM manufacturer WHERE id = ?', (manufacturer_id,)).fetchone()
    cursor.close()

    if manufacturer_raw is None:
        return None

    return _create_manufacturer(manufacturer_raw)


def get_all(connection: sqlite3.Connection) -> set[Manufacturer]:
    """
    Get all the manufacturers in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the manufacturers in the database.
    @rtype: set[Manufacturer]
    """
    manufacturers = set()

    cursor = connection.cursor()
    manufacturers_raw = cursor.execute('SELECT * FROM manufacturer').fetchall()
    cursor.close()

    for manufacturer in manufacturers_raw:
        manufacturers.add(_create_manufacturer(manufacturer))

    return manufacturers


def get_all_with_fields(connection: sqlite3.Connection, *fields: str) -> list[dict[str, Any]]:
    data = []
    column_names = ', '.join(fields)

    cursor = connection.cursor()
    manufacturers_raw = cursor.execute(f'SELECT {column_names} FROM manufacturer').fetchall()
    cursor.close()

    for manufacturer in manufacturers_raw:
        dictionary = dict()

        for idx, field in enumerate(fields):
            dictionary[field] = manufacturer[idx]

        data.append(dictionary)

    return data
