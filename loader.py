import sqlite3
from pathlib import Path
import pandas as pd


CLEAN = Path('data/clean_products.csv')
DB = Path('data/output.db')
TABLE = 'products'


SCHEMA = f'''
CREATE TABLE IF NOT EXISTS {TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT,
    price REAL,
    product_url TEXT,
    scraped_at TEXT
);
'''




def run():
    if not CLEAN.exists():
        raise FileNotFoundError(f"Clean file not found: {CLEAN}")


    df = pd.read_csv(CLEAN)


    conn = sqlite3.connect(str(DB))
    cur = conn.cursor()
    cur.executescript(SCHEMA)


    inserted = 0
    for _, row in df.iterrows():
        cur.execute(f"INSERT INTO {TABLE} (name, brand, price, product_url, scraped_at) VALUES (?, ?, ?, ?, ?)", (
            row.get('name'), row.get('brand'), row.get('price'), row.get('product_url'), row.get('scraped_at')
        ))
        inserted += 1


    conn.commit()
    conn.close()
    print(f"Inserted {inserted} rows into {DB}:{TABLE}")




if __name__ == '__main__':
    run()
