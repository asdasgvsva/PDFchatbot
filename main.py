import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from document_processor import DocumentProcessor
from qa_chain import QAChain
from config import *
import uuid
from datetime import datetime
from dotenv import load_dotenv
import tempfile
load_dotenv()

app = FastAPI(
    title="RAG 문서 QA API",
    description="문서 업로드 및 질의응답을 위한 RESTful API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (UI용)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 글로벌 상태 (세션 기반)
sessions: Dict[str, Dict[str, Any]] = {}

# Pydantic 모델들
class QARequest(BaseModel):
    question: str
    k: Optional[int] = 4
    session_id: str

class UploadResponse(BaseModel):
    session_id: str
    message: str
    document_count: int
    chunk_count: int
    uploaded_at: str

class QAResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    question: str
    session_id: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

class SessionInfo(BaseModel):
    session_id: str
    document_count: int
    chunk_count: int
    uploaded_at: str
    is_active: bool

@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("static/index.html")

@app.get("/api", response_class=JSONResponse)
async def api_info():
    """API 정보 엔드포인트"""
    return {
        "message": "RAG 문서 QA API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload",
            "ask": "/ask",
            "sessions": "/sessions",
            "session": "/session/{session_id}",
            "delete_session": "/session/{session_id}"
        }
    }

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """문서 업로드 및 벡터 저장소 생성"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="파일이 선택되지 않았습니다.")
    
    # 지원하는 파일 형식 확인
    allowed_extensions = ['.pdf', '.txt', '.docx', '.md']
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(allowed_extensions)}"
        )
    
    # 세션 ID 생성
    session_id = str(uuid.uuid4())
    
    try:
        # 임시 파일 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # 문서 처리
        doc_processor = DocumentProcessor()
        documents = doc_processor.load_documents(tmp_file_path)
        chunks = doc_processor.split_documents(documents)
        doc_processor.create_vectorstore(chunks)
        qa_chain = QAChain(doc_processor)
        
        # 세션 정보 저장
        sessions[session_id] = {
            "doc_processor": doc_processor,
            "qa_chain": qa_chain,
            "document_count": len(documents),
            "chunk_count": len(chunks),
            "uploaded_at": datetime.now().isoformat(),
            "filename": file.filename
        }
        
        # 임시 파일 삭제
        os.unlink(tmp_file_path)
        
        return UploadResponse(
            session_id=session_id,
            message=f"{len(documents)}개 문서, {len(chunks)}개 청크 저장 완료",
            document_count=len(documents),
            chunk_count=len(chunks),
            uploaded_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        # 임시 파일 정리
        if 'tmp_file_path' in locals():
            os.unlink(tmp_file_path)
        print("==== EXCEPTION OCCURRED ====", flush=True)
        import traceback
        traceback.print_exc()
        print("==== END OF TRACEBACK ====", flush=True)
        raise HTTPException(status_code=500, detail=f"문서 처리 중 오류가 발생했습니다: {str(e)}")

@app.post("/ask", response_model=QAResponse)
async def ask_question(req: QARequest):
    """질문에 대한 답변 생성"""
    if req.session_id not in sessions:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    
    session = sessions[req.session_id]
    qa_chain = session["qa_chain"]
    
    try:
        # k값 조정
        qa_chain.qa_chain.retriever.search_kwargs["k"] = req.k
        result = qa_chain.answer_question(req.question)
        
        return QAResponse(
            answer=result["answer"],
            sources=result.get("sources", []),
            question=req.question,
            session_id=req.session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"질문 처리 중 오류가 발생했습니다: {str(e)}")

@app.get("/sessions", response_model=List[SessionInfo])
async def list_sessions():
    """활성 세션 목록 조회"""
    session_list = []
    for session_id, session_data in sessions.items():
        session_list.append(SessionInfo(
            session_id=session_id,
            document_count=session_data["document_count"],
            chunk_count=session_data["chunk_count"],
            uploaded_at=session_data["uploaded_at"],
            is_active=True
        ))
    return session_list

@app.get("/session/{session_id}", response_model=SessionInfo)
async def get_session_info(session_id: str):
    """특정 세션 정보 조회"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    
    session_data = sessions[session_id]
    return SessionInfo(
        session_id=session_id,
        document_count=session_data["document_count"],
        chunk_count=session_data["chunk_count"],
        uploaded_at=session_data["uploaded_at"],
        is_active=True
    )

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """세션 삭제"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")
    
    # 벡터 저장소 정리
    session = sessions[session_id]
    if hasattr(session["doc_processor"], 'vectorstore'):
        try:
            if os.path.exists(CHROMA_PERSIST_DIRECTORY):
                shutil.rmtree(CHROMA_PERSIST_DIRECTORY)
        except Exception:
            pass
    
    # 세션 삭제
    del sessions[session_id]
    
    return {"message": "세션이 삭제되었습니다."}

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(sessions)
    } 