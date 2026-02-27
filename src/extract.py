import time
import requests
import yaml

def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def fetch_prices(config: dict, retries: int = 3, backoff: int = 15) -> dict:
    base_url = config["api"]["base_url"]
    currency = config["api"]["currency"]
    ids = ",".join(asset["id"] for asset in config["api"]["assets"])

    url = f"{base_url}/simple/price"
    params = {
        "ids": ids,
        "vs_currencies": currency
    }

    # Implement retry logic for handling rate limits (HTTP 429)
    for attempt in range(1, retries + 1):
        response = requests.get(url, params=params)

        if response.status_code == 429:
            if attempt < retries:
                print(f"Rate limited. Waiting {backoff}s before retry {attempt}/{retries}...")
                time.sleep(backoff)
                continue
            else:
                response.raise_for_status()
    
        response.raise_for_status()
        return response.json()