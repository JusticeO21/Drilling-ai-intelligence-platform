from pydantic import BaseModel
from typing import Optional, List, TypedDict

class Message(TypedDict):
    role: str
    content: str

class ChatRequest(BaseModel):
    session_id: str
    message: Message
    chat_history: Optional[List[Message]] = None


class ChatResponse(BaseModel):
    message: Message
    session_id: str
    model_provider: str
    processing_time: Optional[float] = None


class ChatError(BaseModel):
    error: str
    session_id: Optional[str] = None
    details: Optional[str] = None
