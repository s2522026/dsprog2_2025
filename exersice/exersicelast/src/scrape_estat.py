import os
import time
import pandas as pd
import requests
import sqlite3
from bs4 import BeautifulSoup


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


DATA_DIR = os.path.join(BASE_DIR, "../data")
os.makedirs(DATA_DIR, exist_ok=True)
csv_path = os.path.join(DATA_DIR, "aging_rate.csv")


DB_PATH = os.path.join(BASE_DIR, "../db/estat.db")


url = "https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00200524"
headers = {"User-Agent": "Mozilla/5.0"}

time.sleep(2)
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")


df = pd.DataFrame({
    "year": [2010, 2015, 2020],
    "pref_name": ["全国", "全国", "全国"],
    "aging_rate": [23.0, 26.6, 28.8]
})

df = pd.DataFrame({
    "year": [2020]*5,
    "pref_name": ["東京", "神奈川", "大阪", "愛知", "北海道"],
    "aging_rate": [23.1, 25.2, 27.4, 24.8, 31.0]
})


df.to_csv(csv_path, index=False)
print("CSV保存完了:", csv_path)


conn = sqlite3.connect(DB_PATH)

df.to_sql(
    "prefecture_stats",
    conn,
    if_exists="append",
    index=False
)

conn.close()
print("DBにINSERT完了")
