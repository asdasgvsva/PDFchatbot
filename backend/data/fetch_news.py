import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FINNHUB_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['russell2000']

def fetch_and_store_finnhub_news(tickers, from_date, to_date):
    for ticker in tickers:
        url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from={from_date}&to={to_date}&token={API_KEY}"
        response = requests.get(url)
        data = response.json()
        print(f"{ticker} 뉴스 {len(data) if isinstance(data, list) else '응답 이상'}개")
        if isinstance(data, list) and data:
            for news in data:
                if isinstance(news, dict):
                    news['ticker'] = ticker
                    news['date'] = to_date
            try:
                db.news.insert_many(data)
                print(f"{ticker}: 저장 완료")
            except Exception as e:
                print(f"{ticker}: 저장 중 에러 발생 - {e}")
        else:
            print(f"{ticker}: 뉴스 없음 또는 응답 이상 - 패스")

if __name__ == "__main__":
    from_date = "2024-05-01"
    to_date = "2024-06-30"
    tickers = [doc['ticker'] for doc in db.tickers.find({}, {'_id': 0, 'ticker': 1}) if 'ticker' in doc]
    print(tickers[:5])    

fetch_and_store_finnhub_news(tickers, from_date, to_date)