import sqlite3
from datetime import date
from unittest import TestCase

from src.models import employee


class Test(TestCase):
    def setUp(self):
        self.connection = sqlite3.connect('../static/test.db')

    def tearDown(self):
        self.connection.close()

    def test_get_all_ids(self):
        self.assertEqual({1, 2, 3}, employee.get_all_ids(self.connection))

    def test_get_by_id(self):
        employee_1 = employee.Employee(
            1, 'Michael', 'Johnson', '333-444-5555', 'michael.j@example.com', '123 Elm St', 'M', date(1985, 7, 20),
            date(2019, 1, 15), 'Sales Rep', 3000.0, 'pass@word1', True, False
        )

        self.assertEqual(employee_1, employee.get_by_id(self.connection, 1))
        self.assertIsNone(employee.get_by_id(self.connection, 100_000))

    def test_get_all(self):
        employees = {employee.get_by_id(self.connection, id_) for id_ in employee.get_all_ids(self.connection)}
        self.assertEqual(employees, employee.get_all(self.connection))
