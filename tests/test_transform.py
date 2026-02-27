import unittest
from src.transform import transform_prices

MOCK_CONFIG = {
    "api": {
        "currency": "usd",
        "assets": [
            {"id": "bitcoin", "symbol": "BTC"},
            {"id": "cardano", "symbol": "ADA"}
            ]
    }
}

MOCK_RAW_DATA = {
    "bitcoin": {"usd": 67000.0},
    "cardano": {"usd": 0.29}
}

class TestTransformPrices(unittest.TestCase):
    def setUp(self):
        self.records = transform_prices(MOCK_RAW_DATA, MOCK_CONFIG)
    
    def test_returns_correct_number_of_records(self):
        self.assertEqual(len(self.records), 2)
    
    def test_btc_symbol_map_correctly(self):
        btc = next(r for r in self.records if r["symbol"] == "BTC")
        self.assertEqual(btc["price"], 67000.0)

    def test_ada_symbol_map_correctly(self):
        ada = next(r for r in self.records if r["symbol"] == "ADA")
        self.assertEqual(ada["price"], 0.29)
    
    def test_records_contain_req_keys(self):
        for record in self.records:
            self.assertIn("date", record)
            self.assertIn("time", record)
            self.assertIn("symbol", record)
            self.assertIn("price", record)
    
    def test_date_format(self):
        for record in self.records:
            self.assertRegex(record["date"], r"^\d{4}-\d{2}-\d{2}$")
    
    def test_time_format(self):
        for record in self.records:
            self.assertRegex(record["time"], r"^\d{2}:\d{2}:\d{2}$")
    
if __name__ == "__main__":
    unittest.main()