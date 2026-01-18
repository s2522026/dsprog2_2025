import sqlite3
import pandas as pd

conn = sqlite3.connect("db/estat.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS prefecture_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pref_name TEXT,
    year INTEGER,
    aging_rate REAL,
    medical_cost REAL
)
""")

df = pd.read_csv("data/aging_rate.csv")
df.to_sql("prefecture_stats", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("DB initialized")
