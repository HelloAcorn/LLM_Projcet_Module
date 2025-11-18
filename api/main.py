from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path
from typing import List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

app = FastAPI(
    title="LLM Project Module API",
    description="범용 Prompt Engineering 및 RAG API",
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

# ============ 데이터 모델 ============

class PromptRequest(BaseModel):
    query: str
    temperature: float = 0.7
    max_tokens: int = 1000

class PromptResponse(BaseModel):
    query: str
    response: str
    model: str
    tokens_used: int

class RAGRequest(BaseModel):
    query: str
    top_k: int = 5
    use_reranker: bool = False

class RAGResponse(BaseModel):
    query: str
    answer: str
    sources: List[dict]
    confidence: float

class AgentRequest(BaseModel):
    task: str
    agent_type: str = "react"
    tools: List[str] = []

class AgentResponse(BaseModel):
    task: str
    result: str
    steps: List[dict]
    success: bool

# ============ 헬스 체크 ============

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "service": "LLM Project Module API"
    }

# ============ Simple Prompt API ============

@app.post("/api/v1/prompt", response_model=PromptResponse)
async def simple_prompt(request: PromptRequest):
    """
    기본 LLM 프롬프트 실행
    
    - **query**: 사용자 질문
    - **temperature**: 응답 창의성 (0.0-1.0)
    - **max_tokens**: 최대 생성 토큰
    """
    try:
        # LLM 호출 로직
        response = f"'{request.query}'에 대한 응답"
        
        return PromptResponse(
            query=request.query,
            response=response,
            model="gpt-4",
            tokens_used=150
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ RAG API ============

@app.post("/api/v1/rag/search", response_model=RAGResponse)
async def rag_search(request: RAGRequest):
    """
    RAG 문서 검색
    
    - **query**: 검색 쿼리
    - **top_k**: 반환할 최상위 문서 개수
    - **use_reranker**: Re-ranker 사용 여부
    """
    try:
        answer = f"'{request.query}'에 대한 RAG 기반 답변"
        sources = [
            {"id": 1, "content": "문서 1", "relevance": 0.95},
            {"id": 2, "content": "문서 2", "relevance": 0.87}
        ]
        
        return RAGResponse(
            query=request.query,
            answer=answer,
            sources=sources,
            confidence=0.92
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/rag/documents")
async def add_documents(files: List[str]):
    """
    RAG 인덱스에 문서 추가
    
    - **files**: 업로드된 파일 경로 리스트
    """
    return {
        "status": "success",
        "documents_added": len(files),
        "message": f"{len(files)}개의 문서가 추가되었습니다."
    }

# ============ 에이전트 API ============

@app.post("/api/v1/agent/execute", response_model=AgentResponse)
async def execute_agent(request: AgentRequest):
    """
    에이전트 작업 실행
    
    - **task**: 실행할 작업 설명
    - **agent_type**: 에이전트 타입 (react, plan_execute, reflection)
    - **tools**: 사용 가능한 도구 리스트
    """
    try:
        steps = [
            {"step": 1, "action": "분석", "observation": "작업 분석 완료"},
            {"step": 2, "action": "실행", "observation": "작업 실행 완료"}
        ]
        
        return AgentResponse(
            task=request.task,
            result="작업이 성공적으로 완료되었습니다.",
            steps=steps,
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ 설정 API ============

@app.get("/api/v1/config")
async def get_config():
    """현재 설정 조회"""
    return {
        "llm_model": "gpt-4",
        "embedding_model": "text-embedding-3-large",
        "vectorstore": "faiss",
        "temperature": 0.7,
        "max_tokens": 1000
    }

@app.put("/api/v1/config")
async def update_config(config: dict):
    """설정 업데이트"""
    return {
        "status": "success",
        "message": "설정이 업데이트되었습니다.",
        "config": config
    }

# ============ 모델 정보 API ============

@app.get("/api/v1/models/llm")
async def list_llm_models():
    """사용 가능한 LLM 모델 조회"""
    return {
        "models": [
            {"name": "gpt-4", "provider": "OpenAI", "context_window": 128000},
            {"name": "gpt-3.5-turbo", "provider": "OpenAI", "context_window": 4096},
            {"name": "claude-3-opus", "provider": "Anthropic", "context_window": 200000},
            {"name": "claude-3-sonnet", "provider": "Anthropic", "context_window": 200000}
        ]
    }

@app.get("/api/v1/models/embedding")
async def list_embedding_models():
    """사용 가능한 Embedding 모델 조회"""
    return {
        "models": [
            {"name": "text-embedding-3-large", "provider": "OpenAI", "dimension": 3072},
            {"name": "bge-base-en-v1.5", "provider": "HuggingFace", "dimension": 768},
            {"name": "e5-large", "provider": "HuggingFace", "dimension": 1024}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

