from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path
from typing import List, Optional
import time
import json
import os
from datetime import datetime

# Add src to path and alias 'src' to 'app'
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Alias 'src' to 'app' to satisfy internal imports like 'from app.core...'
import src
sys.modules["app"] = src

from src.llm.llm_factory import LLMFactory
from langchain.schema import SystemMessage, HumanMessage

app = FastAPI(
    title="LLM Project Module API",
    description="Standard Chat API using LLMFactory",
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

# ============ Logging Middleware ============
LOG_FILE = Path(__file__).parent.parent / "logs/api_requests.jsonl"
os.makedirs(LOG_FILE.parent, exist_ok=True)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # ms
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "latency_ms": round(process_time, 2)
    }
    
    # Log API and health check requests
    if "/api/" in request.url.path or request.url.path == "/health":
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Failed to write log: {e}")
            
    return response

# ============ Data Models ============

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    chat_list: List[Message]
    user_message: str
    uid: Optional[str] = None
    lang: Optional[str] = "ko"
    model: str = "gemini-2.5-flash-lite"
    temperature: float = 0.7

class ChatResponse(BaseModel):
    responses: List[str]

# ============ Health Check ============

@app.get("/health")
async def health_check():
    """Health Check Endpoint"""
    return {
        "status": "healthy",
        "service": "LLM Project Module API"
    }

# ============ Chat API ============

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat API using LLMFactory
    """
    try:
        # Determine provider based on model name
        if "gpt" in request.model:
            provider = "openai"
        elif "claude" in request.model:
            provider = "anthropic"
        elif "gemini" in request.model:
            provider = "gemini"
        else:
            provider = "openai"

        # Create LLM
        llm = LLMFactory.create(
            provider=provider,
            model=request.model,
            temperature=request.temperature
        )

        # Prepare messages
        messages = []
        for msg in request.chat_list:
            if msg.role == "user":
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                messages.append(SystemMessage(content=msg.content))
        
        # Add current user message
        messages.append(HumanMessage(content=request.user_message))

        # Invoke LLM
        response = llm.invoke(messages)
        
        full_response = ""
        if isinstance(response, dict) and "parsed" in response:
            parsed = response["parsed"]
            if parsed and hasattr(parsed, 'response'):
                full_response = parsed.response
        elif hasattr(response, 'response'):
            full_response = response.response
        else:
            full_response = str(response)

        return ChatResponse(responses=[full_response])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
