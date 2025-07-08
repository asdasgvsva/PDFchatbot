# Russell 2000 RAG 기반 뉴스/챗봇 서비스

이 프로젝트는 Russell 2000(미국 소형주 지수) 관련 최신 뉴스와 RAG(Retrieval-Augmented Generation) 기반 챗봇을 제공하는 서비스입니다. 실시간 지수, 환율, 뉴스, 그리고 자연어 질의응답 기능을 갖춘 실제 서비스 수준의 웹앱을 목표로 합니다.

## 주요 기능
- Russell 2000, S&P500, 환율 등 주요 지수 실시간 표시
- Russell 2000 종목별/전체 뉴스 수집 및 요약
- 뉴스/공시/문서 기반 RAG 챗봇(질문→최신 정보 기반 답변)
- 번역(영문→한국어) 지원
- 반응형 UI/UX

## 기술 스택
- **백엔드**: FastAPI, Python, MongoDB, ChromaDB, OpenAI API, yfinance, Finnhub, Alpha Vantage
- **프론트엔드**: React, TypeScript, styled-components, recharts, axios
- **번역**: Google 번역 API 또는 파파고
- **배포**: Docker, docker-compose

## 폴더 구조
```
backend/
  main.py
  requirements.txt
  data/
    fetch_tickers.py
    fetch_indices.py
    fetch_news.py
  rag/
    embedding.py
    retrieval.py
    chatbot.py
  db/
    mongo.py
    chroma.py
  utils/
    translate.py
frontend/
  src/
    components/
      Header.tsx
      IndicesBar.tsx
      NewsList.tsx
      Chatbot.tsx
    App.tsx
    index.tsx
  package.json
  tsconfig.json
docker-compose.yml
README.md
```

## 개발 단계
1. 프로젝트 구조/환경 세팅
2. 데이터 수집(티커, 지수, 뉴스)
3. 백엔드 API 구현
4. 임베딩/벡터DB/RAG 파이프라인
5. 번역 API 연동
6. 프론트엔드 UI/UX 및 API 연동
7. 통합 테스트/예산 검토
8. 배포/운영

---
각 단계별로 코드와 설명을 추가하며 진행합니다.
