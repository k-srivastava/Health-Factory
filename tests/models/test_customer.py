import sqlite3
from datetime import date
from unittest import TestCase

from src.models import customer


class Test(TestCase):
    def setUp(self):
        self.connection = sqlite3.connect('../static/test.db')

    def tearDown(self):
        self.connection.close()

    def test_get_all_ids(self):
        self.assertEqual({1, 2, 3}, customer.get_all_ids(self.connection))

    def test_get_by_id(self):
        customer_1 = customer.Customer(
            1, 'Mary', 'Johnson', '111-222-3333', 'mary.j@example.com', '789 Maple St', 'F',
            date(1980, 3, 15)
        )

        self.assertEqual(customer_1, customer.get_by_id(self.connection, 1))
        self.assertIsNone(customer.get_by_id(self.connection, 100_000))

    def test_get_all(self):
        customers = {customer.get_by_id(self.connection, id_) for id_ in customer.get_all_ids(self.connection)}
        self.assertEqual(customers, customer.get_all(self.connection))

