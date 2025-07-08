import os
from pymongo import MongoClient
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
client = MongoClient(MONGO_URL)
db = client["russell2000"]

def get_quote(ticker):
    url = f"{FINNHUB_BASE_URL}/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
    return requests.get(url).json()

def batch_update_quotes():
    tickers = [doc['ticker'] for doc in db.tickers.find({}, {'_id': 0, 'ticker': 1}) if 'ticker' in doc]
    skipped_tickers = []
    today = datetime.utcnow().strftime("%Y-%m-%d")
    for ticker in tickers:
        data = get_quote(ticker)
        if not isinstance(data, dict) or "c" not in data:
            print(f"{ticker}: quote 데이터 이상, 건너뜀. 응답: {data}")
            skipped_tickers.append(ticker)
            continue
        # 이미 있으면 건너뜀
        if db.quotes.find_one({"ticker": ticker, "date": today}):
            continue
        db.quotes.insert_one({
            "ticker": ticker,
            "date": today,
            "quote": data,
            "updated_at": datetime.utcnow()
        })
        print(f"{ticker} 저장 완료")
    print("\n=== 건너뛴 ticker 목록 ===")
    for t in skipped_tickers:
        print(t)

if __name__ == "__main__":
    batch_update_quotes()