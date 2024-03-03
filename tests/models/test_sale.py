import sqlite3
from datetime import datetime
from unittest import TestCase

from src.models import sale


class Test(TestCase):
    def setUp(self):
        self.connection = sqlite3.connect('../static/test.db')

    def tearDown(self):
        self.connection.close()

    def test_get_all_ids(self):
        self.assertEqual({1, 2, 3}, sale.get_all_ids(self.connection))

    def test_get_by_id(self):
        sale_1 = sale.Sale(1, datetime(2024, 2, 24, 10, 15, 0), 2, 1, 42)

        self.assertEqual(sale_1, sale.get_by_id(self.connection, 1))
        self.assertIsNone(sale.get_by_id(self.connection, 100_000))

    def test_get_all(self):
        sales = {sale.get_by_id(self.connection, id_) for id_ in sale.get_all_ids(self.connection)}
        self.assertEqual(sales, sale.get_all(self.connection))
