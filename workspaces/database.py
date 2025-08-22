# database.py

import sqlite3

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect('restaurant.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Create the necessary tables for the billing system."""
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                order_type TEXT NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY,
                order_id INTEGER,
                item_id INTEGER,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (item_id) REFERENCES menu_items (id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY,
                order_id INTEGER,
                subtotal REAL NOT NULL,
                tax_amount REAL NOT NULL,
                discount_amount REAL NOT NULL,
                total_amount REAL NOT NULL,
                payment_method TEXT,
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (id)
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def setup_database():
    """Initialize the database and create tables."""
    conn = create_connection()
    if conn:
        create_tables(conn)
        conn.close()

if __name__ == '__main__':
    setup_database()
    
