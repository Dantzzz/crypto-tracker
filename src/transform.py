from datetime import datetime, timezone

def transform_prices(raw_data: dict, config: dict) -> list[dict]:
    now = datetime.now(timezone.utc)     # captures current timestamp in UTC
    date_str = now.strftime("%Y-%m-%d")  #
    time_str = now.strftime("%H:%M:%S")  #

    '''
    dict built from config; maps CG's internal IDs to ticker symbols
    API output: bitcoin --> convert to BTC for db
    '''
    symbol_map = {
        asset["id"]: asset["symbol"]
        for asset in config["api"]["assets"]
    }

    '''
    # 
    '''
    records = []
    for asset_id, price_data in raw_data.items():
        records.append({
            "date": date_str,
            "time": time_str,
            "symbol": symbol_map[asset_id],
            "price": price_data[config["api"]["currency"]]
        })
    
    return records