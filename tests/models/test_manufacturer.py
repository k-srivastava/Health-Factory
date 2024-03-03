import sqlite3
from unittest import TestCase

from src.models import manufacturer


class Test(TestCase):
    def setUp(self):
        self.connection = sqlite3.connect('../static/test.db')

    def tearDown(self):
        self.connection.close()

    def test_get_all_ids(self):
        self.assertEqual({1, 2, 3}, manufacturer.get_all_ids(self.connection))

    def test_get_by_id(self):
        manufacturer_2 = manufacturer.Manufacturer(2, 'GlaxoSmithKline', '987-654-3210', None)

        self.assertEqual(manufacturer_2, manufacturer.get_by_id(self.connection, 2))
        self.assertIsNone(manufacturer.get_by_id(self.connection, 100_000))

    def test_get_all(self):
        manufacturers = {
            manufacturer.get_by_id(self.connection, id_) for id_ in manufacturer.get_all_ids(self.connection)
        }

        self.assertEqual(manufacturers, manufacturer.get_all(self.connection))
