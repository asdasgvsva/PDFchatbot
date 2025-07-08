import os
from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['russell2000']

app = FastAPI()

@app.get("/api/news")
def get_news():
    # 최신 뉴스 20개 반환
    return list(db.news.find({}, {"_id": 0}).sort("date", -1).limit(20))

# 필요시 다른 엔드포인트도 여기에 추가
# 예: /api/top-movers, /api/top-themes, /api/indices, /api/chat 등

# 서버 실행: uvicorn main:app --reload --port 8001 