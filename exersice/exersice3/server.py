from flask import Flask, render_template, jsonify
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)
DB_NAME = "weather.db"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/forecast/<area_code>")
def forecast(area_code):
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
    data = requests.get(url).json()

    weather = data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
    area_name = data[0]["publishingOffice"]
    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO weather (area_code, area_name, date, weather, fetched_at)
        VALUES (?, ?, ?, ?, ?)
    """, (area_code, area_name, today, weather, datetime.now()))

    conn.commit()
    conn.close()

    return jsonify({
        "area": area_name,
        "date": today,
        "weather": weather
    })


@app.route("/history/<area_code>/<date>")
def history(area_code, date):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT weather FROM weather
        WHERE area_code = ? AND date = ?
    """, (area_code, date))

    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({"weather": row[0]})
    else:
        return jsonify({"weather": "データなし"})


if __name__ == "__main__":
    app.run(debug=True)
