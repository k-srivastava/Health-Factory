"""Customer model and related functions to query the database."""
import sqlite3
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True, slots=True)
class Customer:
    """Customer model."""
    id: int
    first_name: str
    last_name: str
    phone_number: str
    email_address: Optional[str]
    address: Optional[str]
    gender: Optional[str]
    birth_date: Optional[date]

    @property
    def full_name(self) -> str:
        """
        Generate the full name of the customer using their first and last names.

        @return: Full name of the customer.
        @rtype: str
        """
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self) -> int:
        """
        Calculate the age of the customer using their birthdate.

        @return: Age of the customer.
        @rtype: int

        @raise AttributeError: If the customer's birthdate is None.
        """
        if self.birth_date is None:
            raise AttributeError(f'Cannot calculate age of customer with id {self.id} where birth date is None.')

        current_date = date.today()

        return current_date.year - self.birth_date.year - (
            (current_date.month, current_date.day) < (self.birth_date.month, self.birth_date.day)
        )


def _create_customer(raw_data: tuple) -> Customer:
    """
    Create a customer object from a record returned from the database.

    @param raw_data: Data returned from the database from the customer table.
    @type raw_data: tuple

    @return: Customer object from the database.
    @rtype: Customer
    """
    return Customer(
        id=raw_data[0],
        first_name=raw_data[1],
        last_name=raw_data[2],
        phone_number=raw_data[3],
        email_address=None if raw_data[4] == '' else raw_data[4],
        address=None if raw_data[5] == '' else raw_data[5],
        gender=None if raw_data[6] == '' else raw_data[6],
        birth_date=None if raw_data[7] == '' else date.fromisoformat(raw_data[7])
    )


def get_all_ids(connection: sqlite3.Connection) -> set[int]:
    """
    Get all the IDs of the customers in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the IDs of the customers in the database.
    @rtype: set[int]
    """
    cursor = connection.cursor()
    ids: list[tuple[int]] = cursor.execute('SELECT id FROM customer').fetchall()
    cursor.close()

    return {id_[0] for id_ in ids}


def get_by_id(connection: sqlite3.Connection, customer_id: int) -> Optional[Customer]:
    """
    Get the customer by its unique ID.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection
    @param customer_id: Customer ID.
    @type customer_id: int

    @return: Customer in the database, or None if the customer does not exist.
    @rtype: Optional[Customer]
    """
    cursor = connection.cursor()
    customer_raw = cursor.execute('SELECT * FROM customer WHERE id = ?', (customer_id,)).fetchone()
    cursor.close()

    if customer_raw is None:
        return None

    return _create_customer(customer_raw)


def get_all(connection: sqlite3.Connection) -> set[Customer]:
    """
    Get all the customers in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the customers in the database.
    @rtype: set[Customer]
    """
    customers = set()

    cursor = connection.cursor()
    customers_raw = cursor.execute('SELECT * FROM customer').fetchall()
    cursor.close()

    for customer in customers_raw:
        customers.add(_create_customer(customer))

    return customers
