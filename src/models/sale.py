"""Sale model and related functions to query the database."""
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

from models import employee, customer


@dataclass(frozen=True, slots=True)
class Sale:
    """Sale model."""
    id: int
    date_time: datetime
    employee_id: int
    customer_id: int
    amount: float

    def employee(self, connection: sqlite3.Connection) -> employee.Employee:
        """
        Get the employee object related to the sale.

        @param connection: Connection to the database.
        @type connection: sqlite3.Connection

        @return: Employee object represented by the foreign key in the sale.
        @rtype: employee.Employee
        """
        return employee.get_by_id(connection, self.employee_id)

    def customer(self, connection: sqlite3.Connection) -> customer.Customer:
        """
        Get the customer object related to the sale.

        @param connection: Connection to the database.
        @type connection: sqlite3.Connection

        @return: Customer object represented by the foreign key in the sale.
        @rtype: customer.Customer
        """
        return customer.get_by_id(connection, self.customer_id)


def _create_sale(raw_data: tuple) -> Sale:
    """
    Create a sale object from a record returned from the database.

    @param raw_data: Data from the database from the sale table.
    @type raw_data: tuple

    @return: Sale object from the database.
    @rtype: Sale
    """
    return Sale(
        id=raw_data[0],
        date_time=datetime.fromisoformat(raw_data[1]),
        employee_id=raw_data[2],
        customer_id=raw_data[3],
        amount=float(raw_data[4])
    )


def get_all_ids(connection: sqlite3.Connection) -> set[int]:
    """
    Get all the IDs of the sales in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the IDs of the sales in the database.
    @rtype: set[int]
    """
    cursor = connection.cursor()
    ids: list[tuple[int]] = cursor.execute('SELECT id FROM sale').fetchall()
    cursor.close()

    return {id_[0] for id_ in ids}


def get_by_id(connection: sqlite3.Connection, sale_id: int) -> Optional[Sale]:
    """
    Get the sale by its unique ID.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection
    @param sale_id: Sale ID.
    @type sale_id: int

    @return: Sale in the database, or None if the sale does not exist.
    @rtype: Optional[Sale]
    """
    cursor = connection.cursor()
    sale_raw = cursor.execute('SELECT * FROM sale WHERE id = ?', (sale_id,)).fetchone()
    cursor.close()

    if sale_raw is None:
        return None

    return _create_sale(sale_raw)


def get_all(connection: sqlite3.Connection) -> set[Sale]:
    """
    Get all the sales in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the sales in the database.
    @rtype: set[Sale]
    """
    sales = set()

    cursor = connection.cursor()
    sales_raw = cursor.execute('SELECT * FROM sale').fetchall()
    cursor.close()

    for sale in sales_raw:
        sales.add(_create_sale(sale))

    return sales


def get_all_with_fields(connection: sqlite3.Connection, *fields: str) -> list[dict[str, Any]]:
    data = []
    column_names = ', '.join(fields)

    cursor = connection.cursor()
    sales_raw = cursor.execute(f'SELECT {column_names} FROM sale').fetchall()
    cursor.close()

    for sale in sales_raw:
        dictionary = dict()

        for idx, field in enumerate(fields):
            dictionary[field] = sale[idx]

        data.append(dictionary)

    return data
