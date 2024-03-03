import sqlite3
from datetime import date
from unittest import TestCase

from src.models import medicine


class Test(TestCase):
    def setUp(self):
        self.connection = sqlite3.connect('../static/test.db')

    def tearDown(self):
        self.connection.close()

    def test_get_all_ids(self):
        self.assertEqual({1, 2, 3}, medicine.get_all_ids(self.connection))

    def test_get_by_id(self):
        medicine_1 = medicine.Medicine(
            1, 'Lipitor', 1, 15.0, 20.0, 10, 50, date(2023, 5, 15), date(2023, 6, 1), date(2025, 6, 1)
        )

        self.assertEqual(medicine_1, medicine.get_by_id(self.connection, 1))
        self.assertIsNone(medicine.get_by_id(self.connection, 100_000))

    def test_get_all(self):
        medicines = {medicine.get_by_id(self.connection, id_) for id_ in medicine.get_all_ids(self.connection)}
        self.assertEqual(medicines, medicine.get_all(self.connection))
