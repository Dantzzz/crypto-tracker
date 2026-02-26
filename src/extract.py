import requests
import yaml

def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def fetch_prices(config: dict) -> dict:
    base_url = config["api"]["base_url"]
    currency = config["api"]["currency"]
    ids = ",".join(asset["id"] for asset in config["api"]["assets"])

    url = f"{base_url}/simple/price"
    params = {
        "ids": ids,
        "vs_currencies": currency
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()