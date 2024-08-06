import sqlite3
from fastapi import HTTPException
from contextlib import contextmanager


def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            named_has TEXT,
            foreing_id INTEGER
        );
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            named_has TEXT,
            foreing_id INTEGER
        );
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            order_date TEXT,
            delivery_date TEXT,
            delivery_time TEXT,
            location TEXT,
            confirmation_status TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        );
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS order_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        );
        """)

@contextmanager
def get_db():
    conn = sqlite3.connect('database.db')
    try:
        yield conn
    finally:
        conn.close()

