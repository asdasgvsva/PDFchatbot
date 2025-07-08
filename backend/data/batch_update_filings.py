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

def get_filings(ticker):
    url = f"{FINNHUB_BASE_URL}/stock/filings?symbol={ticker}&token={FINNHUB_API_KEY}"
    return requests.get(url).json()

def batch_update_filings():
    tickers = [doc['ticker'] for doc in db.tickers.find({}, {'_id': 0, 'ticker': 1}) if 'ticker' in doc]
    skipped_tickers = []
    for ticker in tickers:
        data = get_filings(ticker)
        if not isinstance(data, list):
            print(f"{ticker}: filings 데이터 이상, 건너뜀. 응답: {data}")
            skipped_tickers.append(ticker)
            continue
        any_valid = False
        for filing in data:
            filing_date = filing.get("filingDate")
            if not filing_date:
                continue
            if db.filings.find_one({"ticker": ticker, "filingDate": filing_date}):
                continue
            db.filings.insert_one({
                "ticker": ticker,
                "filingDate": filing_date,
                "filing": filing,
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
    batch_update_filings()