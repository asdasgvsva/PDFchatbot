from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
import os
import sys

# 운영 환경에서는 PYTHONPATH에 backend/data를 추가하는 것이 가장 좋음
sys.path.append('/Users/ha/Desktop/lang/fastapi_rag/backend/data')
from fetch_news import fetch_and_store_finnhub_news, db

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_fetch_news(**context):
    try:
        # Airflow의 execution_date를 사용 (ds: 'YYYY-MM-DD')
        exec_date = context['ds']
        logging.info(f"실행 날짜: {exec_date}")
        # 환경변수 로드 (.env가 Airflow 작업자 환경에 적용되어 있어야 함)
        # tickers 불러오기
        tickers = [doc['ticker'] for doc in db.tickers.find({}, {'_id': 0, 'ticker': 1}) if 'ticker' in doc]
        logging.info(f"티커 개수: {len(tickers)}")
        fetch_and_store_finnhub_news(tickers, exec_date, exec_date)
        logging.info("뉴스 수집 및 번역 완료")
    except Exception as e:
        logging.error(f"Error in run_fetch_news: {e}", exc_info=True)
        raise

with DAG(
    dag_id='fetch_finnhub_news_daily',
    default_args=default_args,
    description='매일 finnhub 뉴스 수집 및 번역',
    schedule_interval='10 0 * * *',  # 매일 00:10
    start_date=datetime(2024, 6, 1),
    catchup=False,
    tags=['news', 'finnhub'],
) as dag:

    fetch_news_task = PythonOperator(
        task_id='fetch_and_translate_news',
        python_callable=run_fetch_news,
    )
