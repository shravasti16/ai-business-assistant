import sqlite3
import pandas as pd

DB_NAME = "tracker.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            project TEXT,
            status TEXT,
            amount REAL,
            deadline TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_client(client_name, project, status, amount, deadline):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "INSERT INTO clients (client_name, project, status, amount, deadline) VALUES (?, ?, ?, ?, ?)",
        (client_name, project, status, amount, str(deadline)),
    )
    conn.commit()
    conn.close()


def get_all_clients():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM clients ORDER BY id DESC", conn)
    conn.close()
    return df


def update_status(row_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("UPDATE clients SET status = ? WHERE id = ?", (new_status, row_id))
    conn.commit()
    conn.close()


def delete_client(row_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM clients WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()