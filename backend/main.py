from fastapi import FastAPI,Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
<<<<<<< HEAD
from data.image_matcher import find_best_image
from data.analysis_news import generate_analysis_report  # analysis_news.py에서 함수 import (경로 수정)

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
UNSPLASH_ACCESS_API_KEY = os.getenv("UNSPLASH_ACCESS_API_KEY") # image

client = MongoClient(MONGO_URL)
db = client["russell2000"]
=======

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD

=======
client = MongoClient(MONGO_URL)
db = client["russell2000"]

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef



@app.get("/api/tickers")
def get_tickers():
    tickers = list(db.tickers.find({}, {"_id": 0}))
    return {"count": len(tickers), "tickers": tickers}

@app.get("/api/indices")
def get_indices():
    indices = [
<<<<<<< HEAD
        {"ticker": "CRDO", "name": "Credo Technology", "change": "+8.2%"},
=======
        {"ticker": "CRDO123", "name": "Credo Technology", "change": "+8.2%"},
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef
        {"ticker": "IONQ", "name": "IonQ Inc.", "change": "+7.5%"},
        {"ticker": "HIMS", "name": "Hims & Hers Health", "change": "+6.9%"},
        {"ticker": "HQY", "name": "HealthEquity", "change": "+6.2%"},
        {"ticker": "FLR", "name": "Fluor Corp.", "change": "+5.8%"},
<<<<<<< HEAD
        {"ticker": "TSLA", "name": "Credo Technology", "change": "+8.2%"},
        {"ticker": "IONQ", "name": "IonQ Inc.", "change": "+7.5%"},
        {"ticker": "HIMS", "name": "Hims & Hers Health", "change": "+6.9%"},
        {"ticker": "HQY", "name": "HealthEquity", "change": "+6.2%"},
        {"ticker": "FLR", "name": "Fluor Corp.", "change": "+5.8%"},
        {"ticker": "CRDO", "name": "Credo Technology", "change": "+8.2%"},
        {"ticker": "IONQ", "name": "IonQ Inc.", "change": "+7.5%"},
        {"ticker": "HIMS", "name": "Hims & Hers Health", "change": "+6.9%"},
        {"ticker": "BYD", "name": "HealthEquity", "change": "+6.2%"},
=======
        {"ticker": "CRDO32", "name": "Credo Technology", "change": "+8.2%"},
        {"ticker": "IONQ", "name": "IonQ Inc.", "change": "+7.5%"},
        {"ticker": "HIMS", "name": "Hims & Hers Health", "change": "+6.9%"},
        {"ticker": "HQY", "name": "HealthEquity", "change": "+6.2%"},
        {"ticker": "FLR3", "name": "Fluor Corp.", "change": "+5.8%"},
        {"ticker": "CRDO", "name": "Credo Technology", "change": "+8.2%"},
        {"ticker": "IONQ", "name": "IonQ Inc.", "change": "+7.5%"},
        {"ticker": "HIMS", "name": "Hims & Hers Health", "change": "+6.9%"},
        {"ticker": "HQY13", "name": "HealthEquity", "change": "+6.2%"},
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef
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

<<<<<<< HEAD
@app.get("/api/news/image")
def get_news_image(headline: str = Query(...)):
    images = list(db.news_image.find({}))
    best_image_url = find_best_image(headline, images)
    return {"image_url": best_image_url}

=======
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef

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

<<<<<<< HEAD
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
=======
    # 4. 뉴스 데이터 (최신순 5개)
    news = list(db.news.find({"related": ticker, "headline_ko": {"$exists": True, "$ne": ""}, "summary_ko": {"$exists": True, "$ne": ""}}, 
                             {"_id": 0, "headline_ko": 1, "summary_ko": 1, "url": 1, "datetime": 1})
                .sort("datetime", -1).limit(5))
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef

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
<<<<<<< HEAD
        {"headline": n.get("headline_ko") or n.get("headline"), "summary": n.get("summary_ko") or n.get("summary"), "url": n["url"], "datetime": n["datetime"]}
=======
        {"headline": n["headline_ko"], "summary": n["summary_ko"], "url": n["url"], "datetime": n["datetime"]}
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef
        for n in news
    ]

    # 6. LLM 분석서 생성 (RAG)
<<<<<<< HEAD
    analysis = generate_analysis_report(news_for_llm, company.get('name', ticker))
=======
    # (여기서는 예시로 프롬프트만, 실제 LLM 연동은 별도 함수로)
    rag_prompt = f"""
아래는 {company.get('name', ticker)}의 최근 실적, 주가, 뉴스 요약입니다.
이 자료를 바탕으로 투자자 관점에서 기업분석서를 작성해줘.

[실적]
{earnings_chart}

[주가]
{price_chart}

[뉴스]
{[n['headline'] for n in news_table]}
"""
    # 실제 LLM 호출 예시 (함수로 분리)
    # analysis = call_llm(rag_prompt)
    analysis = "여기에 LLM이 생성한 기업분석서가 들어갑니다."
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef

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

<<<<<<< HEAD
@app.get("/api/calendar/events")
def get_calendar_events():
    events = list(db.calendar_events.find({}, {"_id": 0}))
    return {"events": events}

=======
>>>>>>> 4dfa035daeb614c7a8807fbc966899c348a475ef
