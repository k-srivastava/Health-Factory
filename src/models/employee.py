"""Employee model and related functions to query the database."""
import sqlite3
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True, slots=True)
class Employee:
    """Employee model."""
    id: int
    first_name: str
    last_name: str
    phone_number: str
    email_address: str
    address: str
    gender: str
    birth_date: date
    joining_date: date
    designation: Optional[str]
    monthly_salary: float
    login_password: str
    currently_employed: bool
    is_administrator: bool

    @property
    def full_name(self) -> str:
        """
        Generate the full name of the employee using their first and last name.

        @return: Full name of the employee.
        @rtype: str
        """
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self) -> int:
        """
        Calculate the age of the employee using their birthdate.

        @return: Age of the employee.
        @rtype: int
        """
        current_date = date.today()
        return current_date.year - self.birth_date.year - (
            (current_date.month, current_date.day) < (self.birth_date.month, self.birth_date.day)
        )


def _create_employee(raw_data: tuple) -> Employee:
    """
    Create an employee object from a record returned from the database.

    @param raw_data: Data returned from the database from the employee table.
    @type raw_data: tuple

    @return: Employee object from the database.
    @rtype: Employee
    """
    return Employee(
        id=raw_data[0],
        first_name=raw_data[1],
        last_name=raw_data[2],
        phone_number=raw_data[3],
        email_address=raw_data[4],
        address=raw_data[5],
        gender=raw_data[6],
        birth_date=date.fromisoformat(raw_data[7]),
        joining_date=date.fromisoformat(raw_data[8]),
        designation=None if raw_data[9] == '' else raw_data[9],
        monthly_salary=float(raw_data[10]),
        login_password=raw_data[11],
        currently_employed=bool(raw_data[12]),
        is_administrator=bool(raw_data[13])
    )


def get_all_ids(connection: sqlite3.Connection) -> set[int]:
    """
    Get all the IDs of the employees in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the IDs of the employees in the database.
    @rtype: set[int]
    """
    cursor = connection.cursor()
    ids: list[tuple[int]] = cursor.execute('SELECT id FROM employee').fetchall()
    cursor.close()

    return {id_[0] for id_ in ids}


def get_by_id(connection: sqlite3.Connection, employee_id: int) -> Optional[Employee]:
    """
    Get the employee by its unique ID.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection
    @param employee_id: Employee ID.
    @type employee_id: int

    @return: Employee in the database, or None if the employee does not exist.
    @rtype: Optional[Employee]
    """
    cursor = connection.cursor()
    employee_raw = cursor.execute('SELECT * FROM employee WHERE id = ?', (employee_id,)).fetchone()
    cursor.close()

    if employee_raw is None:
        return None

    return _create_employee(employee_raw)


def get_all(connection: sqlite3.Connection) -> set[Employee]:
    """
    Get all the employees in the database.

    @param connection: Connection to the database.
    @type connection: sqlite3.Connection

    @return: Set of all the employees in the database.
    @rtype: set[Employee]
    """
    employees = set()

    cursor = connection.cursor()
    employees_raw = cursor.execute('SELECT * FROM employee').fetchall()
    cursor.close()

    for employee in employees_raw:
        employees.add(_create_employee(employee))

    return employees
