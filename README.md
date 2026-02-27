# Simple Crypto Price Tracker

An automated ETL pipeline that collects real-time price snapshots for Bitcoin (BTC) and Cardano (ADA).

## Features

- Fetches live crypto prices every 30 minutes via the CoinGecko free API.
- Stores timestamped snapshots in a local SQLite database (prototype)
- Customizable: Configurable assets, interval, and database path via config/config.yaml.
- Retry logic with backoff API rate limit handling
- Structured logging output to console and file
- Fully containerized for portable deployment

## Project Structure

```bash
crypto-tracker/
├── config/
│   └── config.yaml       # Pipeline configuration
├── data/                 # SQLite database (gitignored)
├── logs/                 # Pipeline logs (gitignored)
├── src/
│   ├── extract.py        # Fetch data from CoinGecko API
│   ├── transform.py      # Reshape raw data into target schema
│   └── load.py           # Write records to SQLite
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── main.py               # Runs one full ETL cycle
├── scheduler.py          # Runs pipeline on a timed interval
├── Dockerfile
└── requirements.txt
```

## Requirements

- Python 3.12+
- Docker (for containerized runs)

## Local Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/crypto-tracker.git
cd crypto-tracker

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage via CLI

**Run a single ETL cycle manually:**

```bash
python3 main.py
```

**Run the scheduler (every 30 minutes):**

```bash
python3 scheduler.py
```

**Run in Docker:**

```bash
docker build -t crypto-tracker .
docker run -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs crypto-tracker
```

## Customizable configuration

- All pipeline settings live in `config/config.yaml`
- Extendible to include other crypto assets by modifying `[assets][id]` and `[assets][symbol]`
- scheduler and database settings are also adjustable.

## Preliminary Database Schema

```sql
CREATE TABLE price_snapshots (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    date    TEXT NOT NULL,
    time    TEXT NOT NULL,
    symbol  TEXT NOT NULL,
    price   REAL NOT NULL
);
```

## Testing

```bash
python3 -m unittest discover tests
```

## Roadmap

- [ ] Deploy to home Linux server via Docker
- [ ] Migrate storage from SQLite to PostgreSQL
- [ ] Add data visualization dashboard
- [ ] Expand to additional crypto assets