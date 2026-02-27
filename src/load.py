import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_conn(config: dict):
    return psycopg2.connect(
        host=config["database"]["host"],
        port=config["database"]["port"],
        dbname=config["database"]["name"],
        user=config["database"]["user"],
        password=os.getenv("DB_PASSWORD")
    )

def init_db(conn, table_name: str) -> None:
    cursor = conn.cursor()
    cursor.execute(f"""
                   CREATE TABLE IF NOT EXISTS {table_name} (
                   id      SERIAL PRIMARY KEY,
                   date    TEXT NOT NULL,
                   time    TEXT NOT NULL,
                   symbol  TEXT NOT NULL,
                   price   REAL NOT NULL
        )
    """)
    conn.commit()
    cursor.close()

# .executemany() over for loop = processes entire batch rather than indiv records
# VALUES syntax shields against sql injection.
def insert_records(conn, table_name: str, records: list[dict]) -> None:
    cursor = conn.cursor()
    cursor.executemany(f"""
        INSERT INTO {table_name} (date, time, symbol, price)
        VALUES (%(date)s, %(time)s, %(symbol)s, %(price)s)
    """, records)    
    conn.commit()
    cursor.close()