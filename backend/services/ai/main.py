"""
AI Service for Oil Drilling Dashboard
Provides AI agents with RAG capabilities for drilling data analysis
"""

from .agents.drilling_agent import DrillingAgent
from .chains.conversation_chain import conversation_manager
from .common.config import ai_settings
from .common.utils import validate_session
from common.logging import logger
from typing import Dict, Any, Optional


class AIService:
    """Main AI service class that coordinates all AI functionality"""

    def __init__(self):
        self.drilling_agent = DrillingAgent()
        logger.info("AI Service initialized with drilling agent")

    def chat_with_data(
        self, session_id: str, message: str, chat_history: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Main chat endpoint that processes user messages with RAG context

        Args:
            session_id: Session ID from data upload
            message: User's message
            chat_history: Optional chat history for context

        Returns:
            Dict with response and metadata
        """

        try:
            # Validate session
            if not validate_session(session_id):
                return {
                    "response": "I'm sorry, but your data session has expired or is invalid. Please upload your data again.",
                    "error": "invalid_session",
                    "session_id": session_id,
                }

            # Process with drilling agent
            response = self.drilling_agent.process_drilling_query(message, session_id)

            logger.info(f"Processed chat message for session {session_id}")

            return {
                "response": response,
                "session_id": session_id,
                "agent": "drilling_agent",
                "model_provider": ai_settings.model_provider,
            }

        except Exception as e:
            logger.error(f"Error in chat_with_data: {e}")
            return {
                "response": f"I apologize, but I encountered an error processing your request: {str(e)}",
                "error": "processing_error",
                "session_id": session_id,
            }

    def get_conversation_response(
        self, session_id: str, message: str, conversation_type: str = "drilling"
    ) -> Dict[str, Any]:
        """
        Get conversational response without RAG context
        Useful for general chat or when no data is uploaded
        """

        try:
            response = conversation_manager.chat(session_id, message, conversation_type)

            return {
                "response": response,
                "session_id": session_id,
                "conversation_type": conversation_type,
                "model_provider": ai_settings.model_provider,
            }

        except Exception as e:
            logger.error(f"Error in conversation: {e}")
            return {
                "response": f"I apologize, but I encountered an error: {str(e)}",
                "error": "conversation_error",
                "session_id": session_id,
            }

    def get_drilling_insights(self, session_id: str) -> Dict[str, Any]:
        """Get automated insights about uploaded drilling data"""

        try:
            if not validate_session(session_id):
                return {
                    "insights": "Session not found or expired. Please upload data again.",
                    "error": "invalid_session",
                }

            insights = self.drilling_agent.get_drilling_insights(session_id)

            return {
                "insights": insights,
                "session_id": session_id,
                "agent": "drilling_agent",
            }

        except Exception as e:
            logger.error(f"Error getting insights: {e}")
            return {
                "insights": f"Error generating insights: {str(e)}",
                "error": "insights_error",
            }

    def clear_conversation(self, session_id: str, conversation_type: str = "drilling"):
        """Clear conversation history for a session"""

        try:
            conversation_manager.clear_conversation(session_id, conversation_type)
            logger.info(f"Cleared conversation for session {session_id}")
            return {"status": "cleared", "session_id": session_id}

        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
            return {"error": str(e), "session_id": session_id}


ai_service = AIService()


def chat_with_drilling_data(session_id: str, message: str) -> str:
    """Simple function to chat with drilling data"""
    result = ai_service.chat_with_data(session_id, message)
    return result.get("response", "Error processing request")


def get_drilling_data_insights(session_id: str) -> str:
    """Simple function to get drilling insights"""
    result = ai_service.get_drilling_insights(session_id)
    return result.get("insights", "Error getting insights")
