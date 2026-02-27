import sqlite3

def get_connection(db_path: str) -> sqlite3.Connection:
    return sqlite3.connect(db_path)

def initialize_database(conn: sqlite3.Connection, table_name: str) -> None:
    cursor = conn.cursor()
    cursor.execute(f"""
                   CREATE TABLE IF NOT EXISTS {table_name} (
                   id      INTEGER PRIMARY KEY AUTOINCREMENT,
                   date    TEXT NOT NULL,
                   time    TEXT NOT NULL,
                   symbol  TEXT NOT NULL,
                   price REAL NOT NULL
        )
    """)
    conn.commit()

def insert_records(conn: sqlite3.Connection, table_name: str, records: list[dict]) -> None:
    cursor = conn.cursor()
    cursor.executemany(f"""
        INSERT INTO {table_name} (date, time, symbol, price)
        VALUES (:date, :time, :symbol, :price) 
    """, records)
    conn.commit()
