from fastapi import APIRouter, HTTPException
from ..schemas import chat as chat_schema
from services.ai.main import ai_service
import time
from common.logging import logger

router = APIRouter()


@router.post("/", response_model=chat_schema.ChatResponse)
async def chat_with_ai(chat_request: chat_schema.ChatRequest):
    """Chat with AI using uploaded drilling data"""

    start_time = time.time()

    try:
        # Call AI service
        result = ai_service.chat_with_data(
            session_id=chat_request.session_id,
            message=chat_request.message["content"],
            chat_history=chat_request.chat_history,
        )

        processing_time = time.time() - start_time

        logger.info(
            f"Chat request processed for session {chat_request.session_id} in {processing_time:.2f}s"
        )

        return chat_schema.ChatResponse(
            message={
                "role": "assistant",
                "content": result.get("response", "No response generated"),
            },
            session_id=chat_request.session_id,
            model_provider=result.get("model_provider", "unknown"),
            processing_time=round(processing_time, 2),
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
