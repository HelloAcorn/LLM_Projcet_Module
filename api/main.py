import time
from typing import List, Optional, Literal
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from src.llm.factory import LLMFactory
from src.utils.logger import logger_manager
from src.prompts.prompt_manager import PromptManager

app = FastAPI(title="LLM Project Module API")

# --- Middleware for Logging ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    logger_manager.log_api_request({
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), # UTC timestamp
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "latency_ms": process_time
    })
    return response

# --- Data Models ---
class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class BasicChatRequest(BaseModel):
    chat_list: List[Message]
    user_message: str
    uid: Optional[str] = None
    lang: Optional[str] = "ko"

class BasicChatResponse(BaseModel):
    responses: List[str]

class NFCChatRequest(BaseModel):
    chat_list: List[Message]
    user_message: str
    lang: str = "ko"
    character_code: int
    team_code: Optional[str] = None
    uuid: Optional[str] = None

class NFCChatResponse(BaseModel):
    responses: List[str]
    emotion: Optional[str] = Field(None, description="joyful, surprise, anger, sadness, encourage, excited, neutral")
    degree: Optional[int] = Field(None, ge=1, le=3)

# --- Endpoints ---

@app.post("/api/v1/chat/basic", response_model=BasicChatResponse)
async def basic_chat(req: BasicChatRequest):
    # Default to OpenAI for basic chat
    llm = LLMFactory.create(provider="openai", json_schema=BasicChatResponse)
    
    # Try to load default system prompt, fallback if not exists
    try:
        system_template = PromptManager.load_template("default_system.yaml")
        system_content = system_template.get("template", "You are a helpful assistant.")
    except Exception:
        system_content = "You are a helpful assistant."

    messages = [SystemMessage(content=system_content)]
    
    for msg in req.chat_list:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        else:
            messages.append(AIMessage(content=msg.content))
    messages.append(HumanMessage(content=req.user_message))
    
    # Invoke
    result = llm.invoke(messages)
    
    # The result should already be parsed into BasicChatResponse by the factory if using structured output
    # However, factory returns instance of the pydantic model OR dict depending on implementation detail.
    # LLMFactory returns BaseChatModel.with_structured_output which returns the Pydantic OBJECT.
    
    return result

@app.post("/api/v1/chat/nfc", response_model=NFCChatResponse)
async def nfc_chat(req: NFCChatRequest):
    # Use OpenAI for NFC by default
    llm = LLMFactory.create(provider="openai", json_schema=NFCChatResponse)
    
    # Load NFC template
    try:
        template_data = PromptManager.load_template("nfc_character.yaml")
        raw_template = template_data.get("template", "")
        # Simple string formatting for now
        system_content = raw_template.format(
            character_code=req.character_code,
            lang=req.lang
        )
    except Exception as e:
        # Fallback
        logger_manager.get_logger().error(f"Failed to load NFC template: {e}")
        system_content = f"You are character {req.character_code}. Speak in {req.lang}."

    messages = [SystemMessage(content=system_content)]
    
    for msg in req.chat_list:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        else:
            messages.append(AIMessage(content=msg.content))
    messages.append(HumanMessage(content=req.user_message))
    
    result = llm.invoke(messages)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

