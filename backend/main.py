from fastapi import FastAPI,Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from data.image_matcher import find_best_image
from data.analysis_news import generate_analysis_report  # analysis_news.py에서 함수 import (경로 수정)

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
UNSPLASH_ACCESS_API_KEY = os.getenv("UNSPLASH_ACCESS_API_KEY") # image

client = MongoClient(MONGO_URL)
db = client["russell2000"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/api/tickers")
def get_tickers():
    tickers = list(db.tickers.find({}, {"_id": 0}))
    return {"count": len(tickers), "tickers": tickers}

@app.get("/api/indices")
def get_indices():
    indices = [
        {"ticker": "CRDO", "name": "Credo Technology", "change": "+8.2%"},
        {"ticker": "IONQ", "name": "IonQ Inc.", "change": "+7.5%"},
        {"ticker": "HIMS", "name": "Hims & Hers Health", "change": "+6.9%"},
        {"ticker": "HQY", "name": "HealthEquity", "change": "+6.2%"},
        {"ticker": "FLR", "name": "Fluor Corp.", "change": "+5.8%"},
        {"ticker": "TSLA", "name": "Credo Technology", "change": "+8.2%"},
        {"ticker": "IONQ", "name": "IonQ Inc.", "change": "+7.5%"},
        {"ticker": "HIMS", "name": "Hims & Hers Health", "change": "+6.9%"},
        {"ticker": "HQY", "name": "HealthEquity", "change": "+6.2%"},
        {"ticker": "FLR", "name": "Fluor Corp.", "change": "+5.8%"},
        {"ticker": "CRDO", "name": "Credo Technology", "change": "+8.2%"},
        {"ticker": "IONQ", "name": "IonQ Inc.", "change": "+7.5%"},
        {"ticker": "HIMS", "name": "Hims & Hers Health", "change": "+6.9%"},
        {"ticker": "BYD", "name": "HealthEquity", "change": "+6.2%"},
        {"ticker": "FLR", "name": "Fluor Corp.", "change": "+5.8%"},
    ]
    return {"indices": indices}

@app.get("/api/news")
def get_news(page: int = Query(1, ge=1), limit: int = Query(15, ge=1)):
    skip = (page - 1) * limit
    # headline_ko, summary_ko가 모두 있는 뉴스만 조회
    query = {"headline_ko": {"$exists": True, "$ne": ""}, "summary_ko": {"$exists": True, "$ne": ""}}
    total_count = db.news.count_documents(query)
    news = list(
        db.news.find(query, {"_id": 0, "headline": 1, "summary": 1, "headline_ko": 1, "summary_ko": 1, "url": 1, "source": 1, "datetime": 1, "image": 1})
        .sort("datetime", -1)
        .skip(skip)
        .limit(limit)
    )
    return {"totalCount": total_count, "news": news}

@app.get("/api/news/image")
def get_news_image(headline: str = Query(...)):
    images = list(db.news_image.find({}))
    best_image_url = find_best_image(headline, images)
    return {"image_url": best_image_url}


@app.get("/api/ticker/earnings")
def api_ticker_earnings(ticker: str):
    if not db.tickers.find_one({"ticker": ticker}):
        raise HTTPException(status_code=404, detail="Ticker not in russell2000 universe")
    data = list(db.earnings.find({"ticker": ticker}, {"_id": 0}))
    if not data:
        raise HTTPException(status_code=404, detail="No earnings data found in DB")
    return {"ticker": ticker, "earnings": data}

def get_earnings(ticker):
    url = f"{FINNHUB_BASE_URL}/stock/earnings?symbol={ticker}&token={FINNHUB_API_KEY}"
    return requests.get(url).json()

def get_quote(ticker):
    url = f"{FINNHUB_BASE_URL}/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
    return requests.get(url).json()

def get_news(ticker, from_date, to_date):
    url = f"{FINNHUB_BASE_URL}/company-news?symbol={ticker}&from={from_date}&to={to_date}&token={FINNHUB_API_KEY}"
    return requests.get(url).json()

def get_filings(ticker):
    url = f"{FINNHUB_BASE_URL}/stock/filings?symbol={ticker}&token={FINNHUB_API_KEY}"
    return requests.get(url).json()

@app.get("/api/ticker/quote")
def api_ticker_quote(ticker: str):
    if not db.tickers.find_one({"ticker": ticker}):
        raise HTTPException(status_code=404, detail="Ticker not in russell2000 universe")
    data = list(db.quotes.find({"ticker": ticker}, {"_id": 0}))
    if not data:
        raise HTTPException(status_code=404, detail="No quote data found in DB")
    return {"ticker": ticker, "quotes": data}

@app.get("/api/ticker/filings")
def api_ticker_filings(ticker: str):
    if not db.tickers.find_one({"ticker": ticker}):
        raise HTTPException(status_code=404, detail="Ticker not in russell2000 universe")
    data = list(db.filings.find({"ticker": ticker}, {"_id": 0}))
    if not data:
        raise HTTPException(status_code=404, detail="No filings data found in DB")
    return {"ticker": ticker, "filings": data}

@app.get("/api/company/list")
def company_list(search: str = ""):  # 검색어는 선택적
    query = {}
    if search:
        # ticker 또는 name에 부분일치 (대소문자 구분 없음)
        query = {"$or": [
            {"ticker": {"$regex": search, "$options": "i"}},
            {"name": {"$regex": search, "$options": "i"}}
        ]}
    companies = list(db.tickers.find(query, {"_id": 0}))
    return {"count": len(companies), "companies": companies}

@app.get("/api/company/analysis")
def company_analysis(ticker: str):
    # 1. 기업 정보
    company = db.tickers.find_one({"ticker": ticker}, {"_id": 0})
    if not company:
        raise HTTPException(status_code=404, detail="기업 정보 없음")

    # 2. 실적 데이터 (최신순 8개)
    earnings = list(db.earnings.find({"ticker": ticker}, {"_id": 0}).sort("period", -1).limit(8))

    # 3. 주가 데이터 (최신순 30개)
    quotes = list(db.quotes.find({"ticker": ticker}, {"_id": 0}).sort("date", -1).limit(30))

    # 4. 뉴스 데이터 (최신순 10개, summary_ko/ko가 없으면 영어 summary 사용)
    news = list(db.news.find({"related": ticker, "$or": [
        {"summary_ko": {"$exists": True, "$ne": ""}},
        {"summary": {"$exists": True, "$ne": ""}}
    ]},
    {"_id": 0, "headline_ko": 1, "headline": 1, "summary_ko": 1, "summary": 1, "url": 1, "datetime": 1})
    .sort("datetime", -1).limit(10))

    # analysis_news.py의 generate_analysis_report에 맞는 필드로 변환
    news_for_llm = []
    for n in news:
        headline = n.get("headline_ko") or n.get("headline") or ""
        summary = n.get("summary_ko") or n.get("summary") or ""
        news_for_llm.append({
            "date": n.get("datetime", ""),
            "headline": headline,
            "summary": summary
        })

    # 5. 차트/표용 데이터 가공 (프론트에서 바로 쓸 수 있게)
    earnings_chart = [
        {"period": e["period"], "actual": e["earnings"].get("actual"), "estimate": e["earnings"].get("estimate")}
        for e in earnings
    ]
    price_chart = [
        {"date": q["date"], "close": q["quote"].get("c")}
        for q in quotes
    ]
    news_table = [
        {"headline": n.get("headline_ko") or n.get("headline"), "summary": n.get("summary_ko") or n.get("summary"), "url": n["url"], "datetime": n["datetime"]}
        for n in news
    ]

    # 6. LLM 분석서 생성 (RAG)
    analysis = generate_analysis_report(news_for_llm, company.get('name', ticker))

    return {
        "company": company,
        "earnings": earnings,
        "quotes": quotes,
        "news": news,
        "analysis": analysis,
        "charts": {
            "earnings_chart": earnings_chart,
            "price_chart": price_chart
        },
        "tables": {
            "earnings_table": earnings_chart,
            "news_table": news_table
        }
    }

@app.get("/api/calendar/events")
def get_calendar_events():
    events = list(db.calendar_events.find({}, {"_id": 0}))
    return {"events": events}

