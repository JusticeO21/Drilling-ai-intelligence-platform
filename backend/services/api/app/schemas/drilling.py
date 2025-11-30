from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class FileProcessingResponse(BaseModel):
    filename: str
    file_type: str
    num_columns: int
    columns: List[str]
    session_id: str


class QueryRequest(BaseModel):
    session_id: str
    question: str
    n_results: Optional[int] = 3


class QueryResponse(BaseModel):
    session_id: str
    question: str
    relevant_chunks: List[str]
    distances: List[float]


class SessionInfo(BaseModel):
    session_id: str
    created_at: str
    expires_at: str
    last_accessed: str
