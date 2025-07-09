import requests
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_API_KEY")
KEYWORDS = ["stock market", "finance", "business", "investment", "chart", "trading", "wall street", "money", "economy"]

def fetch_unsplash_images(query, per_page=30):
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page={per_page}&client_id={ACCESS_KEY}"
    resp = requests.get(url)
    data = resp.json()
    images = []
    for result in data.get('results', []):
        images.append({
            "url": result['urls']['small'],
            "tags": [query],
            "description": result.get('alt_description') or query
        })
    return images

all_images = []
for keyword in KEYWORDS:
    all_images.extend(fetch_unsplash_images(keyword, per_page=30))

# 중복 제거 (url 기준)
unique_images = {img['url']: img for img in all_images}.values()

# DB 저장
client = MongoClient("mongodb://localhost:27017")
db = client["russell2000"]
db.news_image.insert_many(list(unique_images))
print(f"{len(unique_images)}개 이미지가 news_image 컬렉션에 저장되었습니다.")
