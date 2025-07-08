import requests
import pandas as pd
from pymongo import MongoClient
import time
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

INDICES = {
    "RUSSELL2000": {"function": "TIME_SERIES_DAILY", "symbol": "^RUT"},
    "S&P500": {"function": "TIME_SERIES_DAILY", "symbol": "^GSPC"},
    "NASDAQ": {"function": "TIME_SERIES_DAILY", "symbol": "^IXIC"},
    "DOWJONES": {"function": "TIME_SERIES_DAILY", "symbol": "^DJI"},
    "USD_KRW": {"function": "CURRENCY_EXCHANGE_RATE", "from_currency": "USD", "to_currency": "KRW"},
}

def fetch_index(symbol, function, **kwargs):
    params = {"apikey": ALPHA_VANTAGE_API_KEY, "function": function}
    params.update(kwargs)
    if function == "TIME_SERIES_DAILY":
        params["symbol"] = symbol
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data

def fetch_usd_krw():
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": "USD",
        "to_currency": "KRW",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data

def upload_to_mongodb(data, name, mongo_url="mongodb://localhost:27017", db_name="russell2000", col_name="indices"):
    client = MongoClient(mongo_url)
    db = client[db_name]
    col = db[col_name]
    col.update_one({"name": name}, {"$set": {"data": data, "name": name, "updated_at": pd.Timestamp.now()}}, upsert=True)
    print(f"{name} 데이터 업로드 완료")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(MONGO_URL)
db = client["russell2000"]

@app.get("/api/tickers")
def get_tickers():
    tickers = list(db.tickers.find({}, {"_id": 0}))
    return {"count": len(tickers), "tickers": tickers}

@app.get("/api/indices")
def get_indices():
    indices = list(db.indices.find({}, {"_id": 0}))
    return {"indices": indices}

if __name__ == "__main__":
    if not ALPHA_VANTAGE_API_KEY:
        print(".env 파일에 ALPHAVANTAGE_API_KEY가 설정되어 있지 않습니다.")
        exit(1)
    for name, info in INDICES.items():
        if name == "USD_KRW":
            data = fetch_usd_krw()
        else:
            data = fetch_index(info["symbol"], info["function"])
        upload_to_mongodb(data, name)
        time.sleep(15)  # Alpha Vantage 무료 플랜은 1분 5회 제한
