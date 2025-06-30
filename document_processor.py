import os
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import chromadb
from config import *

class DocumentProcessor:
    def __init__(self):
        """문서 처리기 초기화"""
        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )
        self.vectorstore = None
        
    def load_documents(self, file_path: str) -> List[Document]:
        """다양한 형식의 문서를 로드합니다"""
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"지원하지 않는 파일 형식: {file_path}")
        
        return loader.load()
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """문서를 청크로 분할합니다"""
        return self.text_splitter.split_documents(documents)
    
    def create_vectorstore(self, documents: List[Document], collection_name: str = "documents"):
        """문서를 벡터DB에 저장합니다"""
        # Chroma 벡터스토어 생성
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=CHROMA_PERSIST_DIRECTORY,
            collection_name=collection_name
        )
        
        # 벡터스토어 저장
        self.vectorstore.persist()
        print(f"벡터스토어가 {CHROMA_PERSIST_DIRECTORY}에 저장되었습니다.")
        
    def load_existing_vectorstore(self, collection_name: str = "documents"):
        """기존 벡터스토어를 로드합니다"""
        if os.path.exists(CHROMA_PERSIST_DIRECTORY):
            self.vectorstore = Chroma(
                persist_directory=CHROMA_PERSIST_DIRECTORY,
                embedding_function=self.embeddings,
                collection_name=collection_name
            )
            return True
        return False
    
    def search_documents(self, query: str, k: int = 4) -> List[Document]:
        """질문과 관련된 문서를 검색합니다"""
        if not self.vectorstore:
            raise ValueError("벡터스토어가 로드되지 않았습니다.")
        
        return self.vectorstore.similarity_search(query, k=k)
    
    def get_collection_info(self) -> dict:
        """벡터스토어 정보를 반환합니다"""
        if not self.vectorstore:
            return {"status": "not_loaded"}
        
        try:
            collection = self.vectorstore._collection
            count = collection.count()
            return {
                "status": "loaded",
                "document_count": count,
                "collection_name": collection.name
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 