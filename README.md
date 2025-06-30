# RAG 문서 QA 시스템

문서를 업로드하고 AI와 대화할 수 있는 RAG(Retrieval-Augmented Generation) 기반 질의응답 시스템입니다.

## 🚀 주요 기능

### 📄 문서 처리
- **다양한 형식 지원**: PDF, TXT, DOCX, MD 파일 업로드
- **자동 청킹**: 문서를 적절한 크기로 분할하여 벡터 저장소에 저장
- **벡터 검색**: ChromaDB를 사용한 효율적인 유사도 검색

### 💬 AI 대화
- **실시간 질의응답**: 업로드된 문서를 기반으로 한 정확한 답변
- **소스 추적**: 답변의 근거가 되는 문서 청크 표시
- **검색 파라미터 조정**: 검색할 청크 수(k값) 조정 가능

### 📊 표 추출
- **PDF 표 추출**: PDF 파일에서 표 데이터 자동 추출
- **구조화된 데이터**: 추출된 표를 JSON 형태로 제공

### 🎨 현대적인 UI
- **반응형 디자인**: 데스크톱, 태블릿, 모바일 지원
- **드래그 앤 드롭**: 파일 업로드를 위한 직관적인 인터페이스
- **실시간 채팅**: 메시지 형태의 대화 인터페이스
- **세션 관리**: 여러 문서 세션 관리 및 전환

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **LangChain**: LLM 애플리케이션 프레임워크
- **ChromaDB**: 벡터 데이터베이스
- **OpenAI**: GPT 모델 API
- **Sentence Transformers**: 텍스트 임베딩

### Frontend
- **HTML5/CSS3**: 현대적인 웹 표준
- **JavaScript (ES6+)**: 동적 인터페이스
- **Font Awesome**: 아이콘 라이브러리

## 📦 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가하세요:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 서버 실행
```bash
cd fastapi_rag
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 브라우저에서 접속
```
http://localhost:8000
```

## 🔌 API 엔드포인트

### 문서 업로드
```http
POST /upload
Content-Type: multipart/form-data

file: [문서 파일]
```

### 질문하기
```http
POST /ask
Content-Type: application/x-www-form-urlencoded

question: 질문 내용
k: 검색 청크 수 (기본값: 4)
session_id: 세션 ID
```

### 표 추출
```http
POST /extract_table
Content-Type: multipart/form-data

file: [PDF 파일]
```

### 세션 관리
```http
GET /sessions                    # 세션 목록 조회
GET /session/{session_id}        # 특정 세션 정보
DELETE /session/{session_id}     # 세션 삭제
```

### 헬스 체크
```http
GET /health                      # 서버 상태 확인
GET /api                         # API 정보
```

## 🎯 사용 방법

### 1. 문서 업로드
1. 사이드바의 "문서 업로드" 영역에서 파일 선택 또는 드래그 앤 드롭
2. 지원 형식: PDF, TXT, DOCX, MD
3. 업로드 완료 시 세션 ID가 생성되고 채팅이 활성화됩니다

### 2. 질문하기
1. 문서 업로드 후 채팅 입력창에 질문 입력
2. 검색 청크 수 조정 가능 (2, 4, 6, 8개)
3. Enter 키 또는 전송 버튼으로 질문 전송
4. AI 답변과 함께 관련 문서 청크가 표시됩니다

### 3. 표 추출
1. "표 추출" 영역에서 PDF 파일 선택
2. 추출된 표가 모달 창에 표시됩니다
3. 각 표의 페이지 번호와 데이터를 확인할 수 있습니다

### 4. 세션 관리
1. 사이드바에서 활성 세션 목록 확인
2. 세션 클릭으로 전환 가능
3. 세션별로 독립적인 문서 처리

## 🔧 설정 옵션

### config.py에서 조정 가능한 설정
- `CHUNK_SIZE`: 문서 청킹 크기 (기본값: 1000)
- `CHUNK_OVERLAP`: 청크 간 겹침 크기 (기본값: 200)
- `CHROMA_PERSIST_DIRECTORY`: 벡터 저장소 경로
- `EMBEDDING_MODEL`: 임베딩 모델 (기본값: "all-MiniLM-L6-v2")

## 🐳 Docker 실행

```bash
# 이미지 빌드
docker build -t rag-qa-system .

# 컨테이너 실행
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key rag-qa-system
```

## 📱 반응형 디자인

- **데스크톱**: 3열 레이아웃 (사이드바 + 채팅 + 결과)
- **태블릿**: 2열 레이아웃 (사이드바 + 메인 영역)
- **모바일**: 1열 레이아웃 (세로 스택)

## 🔒 보안 고려사항

- 파일 업로드 시 형식 검증
- 세션 기반 상태 관리
- CORS 설정으로 웹 보안 강화
- 임시 파일 자동 정리

## 🚀 성능 최적화

- 비동기 파일 처리
- 벡터 검색 인덱싱
- 메모리 효율적인 청킹
- 정적 파일 캐싱

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 지원

문제가 발생하거나 기능 요청이 있으시면 이슈를 생성해 주세요. 