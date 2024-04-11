"""Sale model and related functions to query the database."""
import sqlite3
from dataclasses import dataclass
from typing import Optional, Any


@dataclass(frozen=True, slots=True)
class Salt:
    """Salt model."""
    id: int
    name: str


def _create_salt(raw_data: tuple) -> Salt:
    """
    Create a salt object from a record returned from the database.

    @param raw_data: Data returned from the database from the salt table.
    @type raw_data: tuple

    @return: Salt object from the database.
    @rtype: Salt
    """
    return Salt(id=raw_data[0], name=raw_data[1])


def get_all_ids(connection: sqlite3.Connection) -> set[int]:
    """
    Get all the IDs of the salts in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the IDs of the salts in the database.
    @rtype: set[int]
    """
    cursor = connection.cursor()
    ids: list[tuple[int]] = cursor.execute('SELECT id from salt').fetchall()
    cursor.close()

    return {id_[0] for id_ in ids}


def get_by_id(connection: sqlite3.Connection, salt_id: int) -> Optional[Salt]:
    """
    Get the salt by its unique ID.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection
    @param salt_id: Salt ID.
    @type salt_id: int

    @return: Salt in the database, or None if the salt does not exist.
    @rtype: Optional[Salt]
    """
    cursor = connection.cursor()
    salt_raw = cursor.execute('SELECT * FROM salt WHERE id = ?', (salt_id,)).fetchone()
    cursor.close()

    if salt_raw is None:
        return None

    return _create_salt(salt_raw)


def get_all(connection: sqlite3.Connection) -> set[Salt]:
    """
    Get all the salts in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the salts in the database.
    @rtype: set[Salt]
    """
    salts = set()

    cursor = connection.cursor()
    salts_raw = cursor.execute('SELECT * FROM salt').fetchall()
    cursor.close()

    for salt in salts_raw:
        salts.add(_create_salt(salt))

    return salts


def get_all_with_fields(connection: sqlite3.Connection, *fields: str) -> list[dict[str, Any]]:
    data = []
    column_names = ', '.join(fields)

    cursor = connection.cursor()
    salts_raw = cursor.execute(f'SELECT {column_names} FROM salt').fetchall()
    cursor.close()

    for salt in salts_raw:
        dictionary = dict()

        for idx, field in enumerate(fields):
            dictionary[field] = salt[idx]

        data.append(dictionary)

    return data
