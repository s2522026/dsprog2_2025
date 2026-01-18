
import sqlite3
import pandas as pd
from pathlib import Path


class EstatAnalyzer:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent
        db_path = base_dir / "db" / "estat.db"
        self.conn = sqlite3.connect(db_path)

    def get_by_year(self, year):
        query = """
        SELECT pref_name, aging_rate
        FROM prefecture_stats
        WHERE year = ?
        ORDER BY aging_rate DESC
        """
        return pd.read_sql(query, self.conn, params=(year,))

    def close(self):
        self.conn.close()
