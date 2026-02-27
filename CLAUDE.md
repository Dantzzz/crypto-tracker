# CLAUDE.md — crypto-tracker

## Project Overview

A Python ETL (Extract-Transform-Load) pipeline for tracking cryptocurrency data. The app periodically fetches crypto prices/data from external APIs, transforms the data, and loads it into local storage.

## Project Structure

```
crypto-tracker/
├── config/config.yaml     # App configuration (API endpoints, intervals, etc.)
├── data/                  # Local data storage (gitkeep placeholder)
├── logs/                  # Runtime log files (gitkeep placeholder)
├── src/
│   ├── extract.py         # Fetch data from crypto APIs
│   ├── transform.py       # Clean and normalize raw data
│   └── load.py            # Persist transformed data to storage
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── main.py                # Application entry point
├── scheduler.py           # Periodic job scheduling
├── requirements.txt       # Python dependencies
└── .env                   # API keys and secrets (not committed)
```

## Architecture

**ETL Pattern:**
1. `extract.py` — Calls CoinGecko's `/simple/price` endpoint with retry logic for rate limits
2. `transform.py` — Maps CoinGecko IDs to ticker symbols, attaches UTC date/time timestamps
3. `load.py` — Writes processed records to a local SQLite database via `executemany`
4. `scheduler.py` — Runs ETL on a configurable interval using APScheduler
5. `main.py` — Sets up logging (file + terminal), orchestrates the ETL call

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run once
python main.py

# Run on a schedule (interval set in config/config.yaml)
python scheduler.py
```

## Testing

```bash
pytest tests/
```

Tests mirror the src/ module structure. Each ETL stage has its own test file.
**Note:** All three test files are currently empty stubs — writing tests is the next priority.

## Configuration

`config/config.yaml` controls all runtime behavior (no secrets):

```yaml
api:
  base_url: "https://api.coingecko.com/api/v3"
  currency: "usd"
  assets:           # add/remove coins here
    - id: "bitcoin"
      symbol: "BTC"
    - id: "cardano"
      symbol: "ADA"

scheduler:
  interval_min: 30  # how often to run the ETL

database:
  path: "data/crypto_prices.db"
  table_name: "price_snapshots"

logging:
  path: "logs/pipeline.log"
```

To track a new coin, add an entry under `assets` using the CoinGecko asset ID and your preferred symbol.

## Development Guidelines

- Keep ETL stages independent — each module should be testable in isolation
- Secrets (API keys, credentials) go in `.env`, never in `config.yaml` or source code
- Configuration (intervals, endpoints, coin lists) goes in `config/config.yaml`
- All persistent data goes under `data/`; all runtime logs go under `logs/`
- Follow the existing file naming conventions: `test_<module>.py` for tests

## Key Files to Know

| File | Purpose |
|------|---------|
| `src/extract.py` | Fetches prices from CoinGecko; 3-retry / 15s backoff on HTTP 429 |
| `src/transform.py` | Maps IDs → symbols, stamps UTC date + time, returns list of dicts |
| `src/load.py` | SQLite: `get_conn`, `init_db`, `insert_records` (batch via executemany) |
| `main.py` | `setup_logging` + `run_etl`; dual-handler logging (file + stdout) |
| `scheduler.py` | APScheduler `BlockingScheduler`; interval read from config |
| `config/config.yaml` | All non-secret runtime config |
| `.env` | Secrets and API keys (not committed) |

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `APScheduler` | 3.11.2 | Periodic job scheduling |
| `requests` | 2.32.5 | HTTP calls to CoinGecko API |
| `PyYAML` | 6.0.3 | Parsing `config/config.yaml` |
| `tzlocal` | 5.3.1 | Local timezone support for APScheduler |

## Status (as of 2026-02-26)

| Component | Status |
|-----------|--------|
| `src/extract.py` | ✅ Complete — CoinGecko fetch with retry logic |
| `src/transform.py` | ✅ Complete — symbol mapping + UTC timestamps |
| `src/load.py` | ✅ Complete — SQLite init + batch insert |
| `main.py` | ✅ Complete — logging setup + ETL orchestration |
| `scheduler.py` | ✅ Complete — APScheduler interval runner |
| `config/config.yaml` | ✅ Configured — BTC, ADA tracked every 30 min |
| `tests/test_extract.py` | ⬜ Not started |
| `tests/test_transform.py` | ⬜ Not started |
| `tests/test_load.py` | ⬜ Not started |

**Next up:** Write tests for all three ETL modules.
