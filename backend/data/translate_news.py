import os
import openai
from pymongo import MongoClient
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['russell2000']

def translate_to_korean(text):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Translate the following English text to Korean:\n\n{text}"}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

def translate_and_update_news():
    # 번역이 안 된 뉴스만 찾기
    news_cursor = db.news.find({
        "$or": [
            {"headline_ko": {"$exists": False}},
            {"summary_ko": {"$exists": False}}
        ]
    })
    for news in news_cursor:
        headline = news.get("headline", "")
        summary = news.get("summary", "")
        if not headline or not summary:
            continue
        try:
            headline_ko = translate_to_korean(headline)
            summary_ko = translate_to_korean(summary)
            db.news.update_one(
                {"_id": news["_id"]},
                {"$set": {"headline_ko": headline_ko, "summary_ko": summary_ko}}
            )
            print(f"번역 완료: {news.get('url', '')}")
        except Exception as e:
            print(f"번역 실패: {e}")

if __name__ == "__main__":
    translate_and_update_news()
