import logging
from src.extract import load_config, fetch_prices
from src.transform import transform_prices
from src.load import get_conn, init_db, insert_records

# Establishes two handlers: terminal and log file (pipeline.log)
def setup_logging(log_path: str) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )

def run_etl(config: dict) -> None:
    table = config["database"]["table_name"]
    log_path = config["logging"]["path"]
    setup_logging(log_path)
    logger = logging.getLogger(__name__)

    try:
        logger.info("Begin process...\n")

        raw = fetch_prices(config)
        logger.info(f"Raw data extraction: {raw}\n")

        records = transform_prices(raw, config)
        logger.info(f"Transformed {len(records)} records.\n")

        conn = get_conn(config)
        init_db(conn, table)
        insert_records(conn, table, records)
        conn.close()

        logger.info("Records loaded successfully. \nETL process complete.")
    except Exception as e:
        logger.error(f"Failure: {e}")
        raise

if __name__ == "__main__":
    config = load_config()
    run_etl(config)