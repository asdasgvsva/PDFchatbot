# backend/data/fetch_calendar_events.py
import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
client = MongoClient(MONGO_URL)
db = client["russell2000"]

# 날짜 범위 지정
from_date = "2025-07-01"
to_date = "2025-07-31"
url = f"https://finnhub.io/api/v1/calendar/earnings?from={from_date}&to={to_date}&token={FINNHUB_API_KEY}"

response = requests.get(url)
data = response.json()

# Finnhub의 earningsCalendar 구조에 따라 데이터 가공
calendar_events = []
for item in data.get("earningsCalendar", []):
    calendar_events.append({
        "date": item["date"],
        "company": item["symbol"],
        "event": "Earnings Call"
    })

# MongoDB에 저장
if calendar_events:
    for item in calendar_events:
        db.calendar_events.update_one(
            {"date": item["date"], "company": item["company"], "event": item["event"]},
            {"$set": item},
            upsert=True
        )
    print(f"Inserted {len(calendar_events)} events.")
else:
    print("No events found.")
