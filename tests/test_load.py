import sqlite3
import unittest
from src.load import init_db, insert_records


MOCK_RECORDS = [
    {"date": "2026-02-26", "time": "21:00:00", "symbol": "BTC", "price": 67000.0},
    {"date": "2026-02-26", "time": "21:00:00", "symbol": "ADA", "price": 0.29}
]

class TestLoad(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        init_db(self.conn, "price_snapshots")

    def tearDown(self):
        self.conn.close()

    def test_table_created(self):
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='price_snapshots'"
        )
        self.assertIsNotNone(cursor.fetchone())

    def test_records_inserted(self):
        insert_records(self.conn, "price_snapshots", MOCK_RECORDS)
        cursor = self.conn.execute("SELECT COUNT(*) FROM price_snapshots")
        self.assertEqual(cursor.fetchone()[0], 2)

    def test_correct_values_stored(self):
        insert_records(self.conn, "price_snapshots", MOCK_RECORDS)
        cursor = self.conn.execute(
            "SELECT symbol, price FROM price_snapshots WHERE symbol = 'BTC'"
        )
        row = cursor.fetchone()
        self.assertEqual(row[0], "BTC")
        self.assertEqual(row[1], 67000.0)

    def test_initialize_is_idempotent(self):
        # Running initialize twice should not raise an error or wipe data
        insert_records(self.conn, "price_snapshots", MOCK_RECORDS)
        init_db(self.conn, "price_snapshots")
        cursor = self.conn.execute("SELECT COUNT(*) FROM price_snapshots")
        self.assertEqual(cursor.fetchone()[0], 2)

if __name__ == "__main__":
    unittest.main()