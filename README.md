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

