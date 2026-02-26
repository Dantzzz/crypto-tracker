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
1. `extract.py` — Calls external crypto APIs (e.g., CoinGecko, CoinMarketCap)
2. `transform.py` — Normalizes, filters, and enriches raw API responses
3. `load.py` — Writes processed records to the data store
4. `scheduler.py` — Orchestrates ETL runs on a schedule
5. `main.py` — Entry point; wires everything together

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env  # add your API keys

# Run once
python main.py

# Run with scheduler
python scheduler.py
```

## Testing

```bash
pytest tests/
```

Tests mirror the src/ module structure. Each ETL stage has its own test file.

## Development Guidelines

- Keep ETL stages independent — each module should be testable in isolation
- Secrets (API keys, credentials) go in `.env`, never in config.yaml or source code
- Configuration (intervals, endpoints, coin lists) goes in `config/config.yaml`
- All persistent data goes under `data/`; all runtime logs go under `logs/`
- Follow the existing file naming conventions: `test_<module>.py` for tests

## Key Files to Know

| File | Purpose |
|------|---------|
| `src/extract.py` | API fetching logic |
| `src/transform.py` | Data normalization |
| `src/load.py` | Storage/persistence |
| `scheduler.py` | Scheduling orchestration |
| `config/config.yaml` | Non-secret configuration |
| `.env` | Secrets and API keys |

## Status

Project is in early scaffolding stage — directory structure and module stubs are in place, implementations are pending.
