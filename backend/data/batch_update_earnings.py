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

def get_earnings(ticker):
    url = f"{FINNHUB_BASE_URL}/stock/earnings?symbol={ticker}&token={FINNHUB_API_KEY}"
    return requests.get(url).json()

def batch_update_earnings():
    tickers = [doc['ticker'] for doc in db.tickers.find({}, {'_id': 0, 'ticker': 1}) if 'ticker' in doc]
    skipped_tickers = []
    for ticker in tickers:
        data = get_earnings(ticker)
        if not isinstance(data, list):
            print(f"{ticker}: API 응답이 리스트가 아님, 건너뜀. 응답: {data}")
            skipped_tickers.append(ticker)
            continue
        any_valid = False
        for earning in data:
            if not isinstance(earning, dict):
                print(f"{ticker}: earning이 dict가 아님, 건너뜀. earning: {earning}")
                continue
            period = earning.get("period")
            if not period:
                continue
            # 이미 있으면 건너뜀
            if db.earnings.find_one({"ticker": ticker, "period": period}):
                continue
            db.earnings.insert_one({
                "ticker": ticker,
                "period": period,
                "earnings": earning,
                "updated_at": datetime.utcnow()
            })
            any_valid = True
        if not any_valid:
            skipped_tickers.append(ticker)
        print(f"{ticker} 저장 완료")
    print("\n=== 건너뛴 ticker 목록 ===")
    for t in skipped_tickers:
        print(t)

if __name__ == "__main__":
    batch_update_earnings()