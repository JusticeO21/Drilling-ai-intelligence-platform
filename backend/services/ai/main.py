from .agents.drilling_data_agent import DrillingDataAgent
from .agents.drilling_data_agent.state import DrillAgentState
from .common.config import ai_settings
from .common.utils import validate_session
from common.logging import logger
from langchain_core.messages import HumanMessage
from typing import Dict, Any, AsyncGenerator

ERROR_MESSAGES = {
    "invalid_session": "I'm sorry, but your data session has expired or is invalid. Please upload your data again.",
    "processing_error": "I apologize, but I encountered an error processing your request: {error}",
    "no_response": "I apologize, but I couldn't process your query.",
}

INSIGHTS_TEMPLATE = """Automated insights are now available through natural language queries. 
Try asking questions like:
- 'What are the main characteristics of my data?'
- 'Show me summary statistics'
- 'What columns have the most missing values?'
- 'Are there any correlations in my data?'"""


def create_agent_state(session_id: str, message: str) -> DrillAgentState:
    """Create DrillAgentState from session and message."""
    return DrillAgentState(
        user_id=session_id,
        dataset_id=f"df_{session_id}",
        messages=[HumanMessage(content=message)],
    )


def create_error_response(
    session_id: str, error_type: str, error_detail: str = ""
) -> Dict[str, Any]:
    """Create standardized error response."""
    message = (
        ERROR_MESSAGES[error_type].format(error=error_detail)
        if error_detail
        else ERROR_MESSAGES[error_type]
    )
    return {
        "response": message,
        "error": error_type,
        "session_id": session_id,
    }


def create_success_response(response: str, session_id: str) -> Dict[str, Any]:
    """Create standardized success response."""
    return {
        "response": response,
        "session_id": session_id,
        "agent": "drill_agent",
        "model_provider": ai_settings.model_provider,
    }


class AIService:
    """Main AI service class that coordinates all AI functionality"""

    def __init__(self):
        self.drill_agent = DrillingDataAgent()
        logger.info("AI Service initialized with drilling data agent")

    def chat_with_drill_ai(self, session_id: str, message: str) -> Dict[str, Any]:
        """
        Process user messages with RAG context using drilling data agent.

        Args:
            session_id: Session ID from data upload
            message: User's message

        Returns:
            Dict with response and metadata
        """
        logger.info(f"Chat request (session: {session_id})")

        try:
            if not validate_session(session_id):
                logger.warning(f"Invalid session: {session_id}")
                return create_error_response(session_id, "invalid_session")

            state = create_agent_state(session_id, message)
            logger.info(f"Starting agent workflow (session: {session_id})")

            result = self.drill_agent.analyze_query(state)
            response = result.get("final_response", ERROR_MESSAGES["no_response"])

            logger.info(
                f"Chat completed (session: {session_id}, length: {len(response)})"
            )
            return create_success_response(response, session_id)

        except Exception as e:
            logger.error(f"Chat error (session: {session_id}): {e}")
            return create_error_response(session_id, "processing_error", str(e))

    async def stream_chat_with_drill_ai(
        self, session_id: str, message: str
    ) -> AsyncGenerator[Dict[str, str], None]:
        """Stream chat responses using uploaded drilling data."""
        logger.info(f"Streaming chat request (session: {session_id})")

        try:
            if not validate_session(session_id):
                logger.warning(f"Invalid session: {session_id}")
                yield {"type": "error", "message": ERROR_MESSAGES["invalid_session"]}
                return

            state = create_agent_state(session_id, message)
            logger.info(f"Starting streaming workflow (session: {session_id})")

            async for chunk in self.drill_agent.stream_analyze_query(state):
                yield chunk

        except Exception as e:
            logger.error(f"Streaming error (session: {session_id}): {e}")
            yield {
                "type": "error",
                "message": ERROR_MESSAGES["processing_error"].format(error=str(e)),
            }

    def get_drilling_insights(self, session_id: str) -> Dict[str, Any]:
        """Get automated insights about uploaded drilling data."""
        try:
            if not validate_session(session_id):
                return create_error_response(session_id, "invalid_session")

            return {
                "insights": INSIGHTS_TEMPLATE,
                "session_id": session_id,
                "agent": "drill_agent",
                "note": "Use chat endpoint for detailed insights",
            }

        except Exception as e:
            logger.error(f"Insights error (session: {session_id}): {e}")
            return {
                "insights": str(e),
                "error": "insights_error",
            }


ai_service = AIService()


def chat_with_drill_ai(session_id: str, message: str) -> str:
    """Simple function to chat with drill AI."""
    result = ai_service.chat_with_drill_ai(session_id, message)
    return result.get("response", "Error processing request")


def get_drill_ai_insights(session_id: str) -> str:
    """Simple function to get drilling insights."""
    result = ai_service.get_drilling_insights(session_id)
    return result.get("insights", "Error getting insights")
