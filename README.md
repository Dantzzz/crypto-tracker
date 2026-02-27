# Simple Crypto Price Tracker

An automated ETL pipeline project that captures real-time price snapshots for Bitcoin (BTC) and Cardano (ADA) using the CoinGecko API. The application structures and stores the data in a PostgreSQL database. The project is highly configurable and fully containerized with Docker.
## Features

- Fetches live crypto prices every 30 minutes via the CoinGecko free API.
- Stores timestamped snapshots in a PostgreSQL database
- Customizable: Configurable assets, interval, and database path via config/config.yaml.
- Retry logic with backoff API rate limit handling
- Structured logging output to console and file
- Fully containerized for portable deployment

## Project Structure

```bash
crypto-tracker/
├── config/
│   └── config.yaml       # Pipeline configuration
├── data/                 # Local data directory (gitignored)
├── logs/                 # Pipeline logs (gitignored)
├── src/
│   ├── extract.py        # Fetch data from CoinGecko API
│   ├── transform.py      # Reshape raw data into target schema
│   └── load.py           # Write records to PostgreSQL
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
- PostgreSQL
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

Create a `.env` file in the project root containing...

```bash
DB_PASSWORD={insert_password}
```

## Database Setup

```sql
CREATE DATABASE crypto_tracker;
CREATE USER user WITH PASSWORD '{insert_password}';
GRANT ALL PRIVILEGES ON DATABASE crypto-tracker TO user;
GRANT ALL ON SCHEMA public TO crypto_user;
```

## Usage via CLI

**Manually run single ETL cycle:**

```bash
python3 main.py
```

**Run scheduler (every 30 minutes):**

```bash
python3 scheduler.py
```

**Run in Docker:**

```bash
docker build -t crypto-tracker .
docker run -d \
    --name crypto-tracker \
    --restart unless-stopped \
    --network host \
    --e DB_PASSWORD={insert_password} \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/logs:/app/logs \
    crypto-tracker
```

## Customizable Configuration

- All pipeline settings contained in `config/config.yaml`
- To track additional assets, add entries to the `assets` list in `config/config.yaml` using their CoinGecko API ID.

## Preliminary Schema

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

- [x] Deploy to home Linux server via Docker
- [x] Migrate storage from SQLite to PostgreSQL
- [ ] Add data visualization dashboard
- [ ] Expand to additional crypto assets