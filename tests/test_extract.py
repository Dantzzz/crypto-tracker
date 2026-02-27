import unittest
from unittest.mock import patch, MagicMock
from src.extract import fetch_prices


MOCK_CONFIG = {
    "api": {
        "base_url": "https://api.coingecko.com/api/v3",
        "currency": "usd",
        "assets": [
            {"id": "bitcoin", "symbol": "BTC"},
            {"id": "cardano", "symbol": "ADA"}
        ]
    }
}

MOCK_API_RESPONSE = {
    "bitcoin": {"usd": 67000.0},
    "cardano": {"usd": 0.29}
}


class TestFetchPrices(unittest.TestCase):

    @patch("src.extract.requests.get")
    def test_returns_expected_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_API_RESPONSE
        mock_get.return_value = mock_response

        result = fetch_prices(MOCK_CONFIG)
        self.assertEqual(result, MOCK_API_RESPONSE)

    @patch("src.extract.requests.get")
    def test_constructs_correct_ids_param(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCK_API_RESPONSE
        mock_get.return_value = mock_response

        fetch_prices(MOCK_CONFIG)
        call_kwargs = mock_get.call_args[1]["params"]
        self.assertIn("bitcoin", call_kwargs["ids"])
        self.assertIn("cardano", call_kwargs["ids"])

    @patch("src.extract.requests.get")
    def test_retries_on_rate_limit(self, mock_get):
        rate_limited = MagicMock()
        rate_limited.status_code = 429

        success = MagicMock()
        success.status_code = 200
        success.json.return_value = MOCK_API_RESPONSE

        mock_get.side_effect = [rate_limited, success]

        result = fetch_prices(MOCK_CONFIG, retries=3, backoff=0)
        self.assertEqual(result, MOCK_API_RESPONSE)


if __name__ == "__main__":
    unittest.main()