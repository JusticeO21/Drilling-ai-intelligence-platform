import pytest
from ..main import AIService, chat_with_drilling_data
from ..common.utils import validate_session


class TestAIService:
    """Test cases for AI service functionality"""

    def test_ai_service_initialization(self):
        """Test that AI service initializes correctly"""
        service = AIService()
        assert service.drilling_agent is not None
        assert service.drilling_agent.name == "DrillingAgent"

    def test_chat_with_invalid_session(self):
        """Test chat with invalid session returns appropriate error"""
        service = AIService()
        result = service.chat_with_data(
            "invalid-session-id", "What is the average depth?"
        )

        assert "error" in result
        assert result["error"] == "invalid_session"
        assert "expired" in result["response"].lower()

    def test_conversation_response(self):
        """Test basic conversation functionality"""
        service = AIService()
        result = service.get_conversation_response("test-session", "Hello")

        assert "response" in result
        assert result["session_id"] == "test-session"
        assert result["conversation_type"] == "drilling"

    def test_clear_conversation(self):
        """Test clearing conversation history"""
        service = AIService()
        result = service.clear_conversation("test-session")

        assert result["status"] == "cleared"
        assert result["session_id"] == "test-session"


def test_chat_with_drilling_data_function():
    """Test the convenience function for chatting with drilling data"""
    # This will fail with invalid session, but tests the function exists
    result = chat_with_drilling_data("invalid-session", "Test question")
    assert isinstance(result, str)
    assert "expired" in result.lower() or "invalid" in result.lower()


def test_validate_session():
    """Test session validation utility"""
    # Invalid session should return False
    assert not validate_session("nonexistent-session")

    # Valid session check would require actual uploaded data
    # This is tested in the integration tests with the API
