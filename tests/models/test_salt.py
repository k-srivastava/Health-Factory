import sqlite3
from unittest import TestCase

from src.models import salt


class Test(TestCase):
    def setUp(self):
        self.connection = sqlite3.connect('../static/test.db')

    def tearDown(self):
        self.connection.close()

    def test_get_all_ids(self):
        self.assertEqual({1, 2, 3, 4, 5}, salt.get_all_ids(self.connection))

    def test_get_by_id(self):
        salt_1 = salt.Salt(1, 'Atorvastatin')

        self.assertEqual(salt_1, salt.get_by_id(self.connection, 1))
        self.assertIsNone(salt.get_by_id(self.connection, 100_000))

    def test_get_all(self):
        salts = {salt.get_by_id(self.connection, id_) for id_ in salt.get_all_ids(self.connection)}
        self.assertEqual(salts, salt.get_all(self.connection))
