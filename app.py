from flask import Flask, jsonify
from datetime import datetime, time
import pandas as pd

app = Flask(__name__)

FILE_NAME = "prayer_times.xlsx"
df = pd.read_excel("prayer_times.xlsx")

def load_data():
    return pd.read_excel(FILE_NAME)

@app.route("/")
def home():
    return "🕌 Prayer Times API is running"

@app.route("/api/data", methods=["GET"])
def get_all_data():
    df['fajr'] = df['fajr'].astype(str)
    df['shuruq'] = df['shuruq'].astype(str)
    df['dhuhr'] = df['dhuhr'].astype(str)
    df['asr'] = df['asr'].astype(str)
    df['maghrib'] = df['maghrib'].astype(str)
    df['isha'] = df['isha'].astype(str)
    return jsonify(df.to_dict(orient="records"))

# 🔹 Get prayer times by city
@app.route("/api/prayer/<city>", methods=["GET"])
def prayer_by_city(city):

    df = load_data()
    df['fajr'] = df['fajr'].astype(str)
    df['shuruq'] = df['shuruq'].astype(str)
    df['dhuhr'] = df['dhuhr'].astype(str)
    df['asr'] = df['asr'].astype(str)
    df['maghrib'] = df['maghrib'].astype(str)
    df['isha'] = df['isha'].astype(str)
    result = df[df["city"].str.lower() == city.lower()]

    if result.empty:
        return jsonify({"error": "City not found"}), 404

    return jsonify(result.to_dict(orient="records"))

# 🔹 Get prayer times by city & date
@app.route("/api/prayer/<city>/<date>", methods=["GET"])
def prayer_by_city_date(city, date):
    df = load_data()
    df['fajr'] = df['fajr'].astype(str)
    df['shuruq'] = df['shuruq'].astype(str)
    df['dhuhr'] = df['dhuhr'].astype(str)
    df['asr'] = df['asr'].astype(str)
    df['maghrib'] = df['maghrib'].astype(str)
    df['isha'] = df['isha'].astype(str)
    result = df[
        (df["city"].str.lower() == city.lower()) &
        (df["date"].astype(str) == date)
    ]

    if result.empty:
        return jsonify({"error": "Data not found"}), 404

    return jsonify(result.to_dict(orient="records")[0])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

