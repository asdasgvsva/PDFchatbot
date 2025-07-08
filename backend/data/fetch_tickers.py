import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient

# Russell 2000 티커 리스트를 Wikipedia에서 크롤링
WIKI_URL = "https://en.wikipedia.org/wiki/List_of_companies_in_the_Russell_2000_Index"


def fetch_russell2000_tickers():
    response = requests.get(WIKI_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})
    tickers = []
    names = []
    sectors = []
    for table in tables:
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 3:
                ticker = cols[0].text.strip()
                name = cols[1].text.strip()
                sector = cols[2].text.strip()
                tickers.append(ticker)
                names.append(name)
                sectors.append(sector)
    df = pd.DataFrame({
        "ticker": tickers,
        "name": names,
        "sector": sectors
    })
    return df


def save_tickers_to_csv(df, filename="russell2000_tickers.csv"):
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} tickers to {filename}")


# 1. CSV 파일 불러오기 및 전처리
def preprocess_tickers(csv_path="russell2000.csv"):
    # 상위 9줄은 메타데이터, 10번째 줄부터 컬럼명
    df = pd.read_csv(csv_path, skiprows=9)
    # 결측치 제거 (티커, 이름)
    df = df.dropna(subset=["Ticker", "Name"])
    # 중복 제거
    df = df.drop_duplicates(subset=["Ticker"])
    # 티커/이름/섹터 공백, 특수문자 정리
    df["Ticker"] = df["Ticker"].apply(lambda x: re.sub(r"[^A-Za-z0-9.-]", "", str(x).strip().upper()))
    df["Name"] = df["Name"].apply(lambda x: str(x).strip())
    if "Sector" in df.columns:
        df["Sector"] = df["Sector"].apply(lambda x: str(x).strip())
    else:
        df["Sector"] = ""
    # MongoDB 업로드용 컬럼명 소문자화
    df = df.rename(columns={"Ticker": "ticker", "Name": "name", "Sector": "sector"})
    return df[["ticker", "name", "sector"]]


# 2. MongoDB에 업로드
def upload_to_mongodb(df, mongo_url="mongodb://localhost:27017", db_name="russell2000", col_name="tickers"):
    client = MongoClient(mongo_url)
    db = client[db_name]
    col = db[col_name]
    # 기존 데이터 삭제 후 업로드
    col.delete_many({})
    records = df.to_dict("records")
    if records:
        col.insert_many(records)
        print(f"업로드 완료: {len(records)}개 티커")
    else:
        print("업로드할 데이터가 없습니다.")


if __name__ == "__main__":
    df = fetch_russell2000_tickers()
    save_tickers_to_csv(df)
    df = preprocess_tickers("russell2000.csv")
    print(df.head())
    upload_to_mongodb(df)
