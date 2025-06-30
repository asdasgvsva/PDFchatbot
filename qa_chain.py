from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from document_processor import DocumentProcessor
from config import *

class QAChain:
    def __init__(self, document_processor: DocumentProcessor):
        """QA 체인 초기화"""
        self.document_processor = document_processor
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            openai_api_key=OPENAI_API_KEY,
            temperature=0.1
        )
        
        # 커스텀 프롬프트 템플릿
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            다음 문서를 참고하여 질문에 답변해주세요.
            
            문서 내용:
            {context}
            
            질문: {question}
            
            답변: 문서 내용을 바탕으로 정확하고 간결하게 답변해주세요. 
            문서에서 찾을 수 없는 정보는 "문서에서 해당 정보를 찾을 수 없습니다."라고 답변해주세요.
            """
        )
        
        # QA 체인 생성
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.document_processor.vectorstore.as_retriever(
                search_kwargs={"k": 8}
            ),
            chain_type_kwargs={"prompt": self.prompt_template},
            return_source_documents=True
        )
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """질문에 대한 답변을 생성합니다"""
        try:
            # QA 체인으로 답변 생성
            result = self.qa_chain({"query": question})
            
            # 소스 문서 정보 추출
            source_documents = result.get("source_documents", [])
            sources = []
            
            for doc in source_documents:
                source_info = {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                }
                sources.append(source_info)
            
            return {
                "answer": result["result"],
                "sources": sources,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "answer": f"오류가 발생했습니다: {str(e)}",
                "sources": [],
                "status": "error"
            }
    
    def get_similar_documents(self, question: str, k: int = 4) -> List[Document]:
        """질문과 유사한 문서를 검색합니다"""
        return self.document_processor.search_documents(question, k) 