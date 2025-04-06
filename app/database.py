import sqlite3

def init_db():
    conn = sqlite3.connect('app/predicoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            distance_from_home REAL,
            distance_from_last_transaction REAL,
            ratio_to_median_purchase_price REAL,
            repeat_retailer INTEGER,
            used_chip INTEGER,
            used_pin_number INTEGER,
            online_order INTEGER,
            predicao INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()