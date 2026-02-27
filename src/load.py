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
