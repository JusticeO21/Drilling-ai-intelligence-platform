import time
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
from ..schemas import chat as chat_schema
from services.ai.main import ai_service
from common.logging import logger

router = APIRouter()

SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
}


def format_sse_event(event_type: str, data: dict) -> str:
    """Format Server-Sent Events message"""
    payload = {"type": event_type, **data}
    return f"data: {json.dumps(payload)}\n\n"


async def stream_chat_generator(
    chat_request: chat_schema.ChatRequest,
) -> AsyncGenerator[str, None]:
    """Generate streaming chat response"""
    try:
        async for event in ai_service.stream_chat_with_drill_ai(
            session_id=chat_request.session_id,
            message=chat_request.message.content,
        ):
            event_type = event["type"]

            if event_type == "status":
                yield format_sse_event("status", {"message": event["message"]})
            elif event_type == "content":
                yield format_sse_event("content", {"delta": event["delta"]})
            elif event_type == "error":
                yield format_sse_event("error", {"message": event["message"]})

    except Exception as e:
        logger.error(f"Streaming chat error (session: {chat_request.session_id}): {e}")
        yield format_sse_event("error", {"message": str(e)})


def create_chat_response(
    result: dict, session_id: str, processing_time: float
) -> chat_schema.ChatResponse:
    """Create standardized chat response"""
    return chat_schema.ChatResponse(
        message={
            "role": "assistant",
            "content": result.get("response", "No response generated"),
        },
        session_id=session_id,
        model_provider=result.get("model_provider", "unknown"),
        processing_time=round(processing_time, 2),
    )


@router.post("/", response_model=chat_schema.ChatResponse)
async def chat_with_ai(chat_request: chat_schema.ChatRequest):
    """Chat with AI using uploaded drilling data"""
    if chat_request.stream:
        return StreamingResponse(
            stream_chat_generator(chat_request),
            media_type="text/event-stream",
            headers=SSE_HEADERS,
        )

    start_time = time.time()

    try:
        result = ai_service.chat_with_drill_ai(
            session_id=chat_request.session_id,
            message=chat_request.message.content,
        )

        processing_time = time.time() - start_time

        logger.info(
            f"Chat processed (session: {chat_request.session_id}, time: {processing_time:.2f}s)"
        )

        return create_chat_response(result, chat_request.session_id, processing_time)

    except Exception as e:
        logger.error(f"Chat error (session: {chat_request.session_id}): {e}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
