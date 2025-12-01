import pytest
from unittest.mock import Mock, patch
from ..main import AIService, chat_with_drill_ai, get_drill_ai_insights, ERROR_MESSAGES, INSIGHTS_TEMPLATE


@pytest.fixture
def mock_validate_session():
    """Fixture to mock validate_session function."""
    with patch('services.ai.main.validate_session') as mock:
        yield mock


@pytest.fixture
def mock_drill_agent():
    """Fixture to mock DrillingDataAgent."""
    with patch('services.ai.main.DrillingDataAgent') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def ai_service(mock_drill_agent):
    """Fixture to create AIService instance with mocked dependencies."""
    return AIService()


class TestAIService:
    """Test cases for AIService class."""

    def test_initialization(self, mock_drill_agent):
        """Test AIService initializes correctly with drilling agent."""
        service = AIService()
        assert service.drill_agent == mock_drill_agent

    def test_chat_with_drill_ai_success(self, ai_service, mock_validate_session, mock_drill_agent):
        """Test successful chat with valid session and agent response."""
        # Setup mocks
        mock_validate_session.return_value = True
        mock_drill_agent.analyze_query.return_value = {"final_response": "Test response"}

        # Test
        result = ai_service.chat_with_drill_ai("valid_session", "What is the average depth?")

        # Assertions
        mock_validate_session.assert_called_once_with("valid_session")
        mock_drill_agent.analyze_query.assert_called_once()
        assert result["response"] == "Test response"
        assert result["session_id"] == "valid_session"
        assert result["agent"] == "drill_agent"
        assert "model_provider" in result

    def test_chat_with_drill_ai_invalid_session(self, ai_service, mock_validate_session):
        """Test chat with invalid session returns error."""
        mock_validate_session.return_value = False

        result = ai_service.chat_with_drill_ai("invalid_session", "Hello")

        mock_validate_session.assert_called_once_with("invalid_session")
        assert result["error"] == "invalid_session"
        assert "expired" in result["response"]
        assert result["session_id"] == "invalid_session"

    @pytest.mark.parametrize("exception,expected_error", [
        (ValueError("Test error"), "processing_error"),
        (RuntimeError("Agent failed"), "processing_error"),
        (Exception("Generic error"), "processing_error"),
    ])
    def test_chat_with_drill_ai_exceptions(self, ai_service, mock_validate_session, mock_drill_agent, exception, expected_error):
        """Test chat handles various exceptions properly."""
        mock_validate_session.return_value = True
        mock_drill_agent.analyze_query.side_effect = exception

        result = ai_service.chat_with_drill_ai("valid_session", "Test message")

        assert result["error"] == expected_error
        assert str(exception) in result["response"]
        assert result["session_id"] == "valid_session"

    def test_chat_with_drill_ai_no_final_response(self, ai_service, mock_validate_session, mock_drill_agent):
        """Test chat when agent returns no final_response."""
        mock_validate_session.return_value = True
        mock_drill_agent.analyze_query.return_value = {}  # No final_response

        result = ai_service.chat_with_drill_ai("valid_session", "Test")

        assert result["response"] == ERROR_MESSAGES["no_response"]
        assert result["session_id"] == "valid_session"

    @pytest.mark.parametrize("message", [
        "",
        "   ",
        "A" * 10000,  # Very long message
        "What is the average depth?",
    ])
    def test_chat_with_drill_ai_edge_cases(self, ai_service, mock_validate_session, mock_drill_agent, message):
        """Test chat with edge case messages."""
        mock_validate_session.return_value = True
        mock_drill_agent.analyze_query.return_value = {"final_response": f"Response to: {message[:50]}..."}

        result = ai_service.chat_with_drill_ai("valid_session", message)

        assert "response" in result
        assert result["session_id"] == "valid_session"

    def test_get_drilling_insights_valid_session(self, ai_service, mock_validate_session):
        """Test getting insights with valid session."""
        mock_validate_session.return_value = True

        result = ai_service.get_drilling_insights("valid_session")

        mock_validate_session.assert_called_once_with("valid_session")
        assert result["insights"] == INSIGHTS_TEMPLATE
        assert result["session_id"] == "valid_session"
        assert result["agent"] == "drill_agent"
        assert "note" in result

    def test_get_drilling_insights_invalid_session(self, ai_service, mock_validate_session):
        """Test getting insights with invalid session."""
        mock_validate_session.return_value = False

        result = ai_service.get_drilling_insights("invalid_session")

        assert result["error"] == "invalid_session"
        assert "expired" in result["response"]

    def test_get_drilling_insights_exception(self, ai_service, mock_validate_session):
        """Test getting insights handles exceptions."""
        mock_validate_session.side_effect = Exception("Redis error")

        result = ai_service.get_drilling_insights("session")

        assert result["insights"] == "Redis error"
        assert result["error"] == "insights_error"


class TestGlobalFunctions:
    """Test cases for global convenience functions."""

    @patch('services.ai.main.ai_service')
    def test_chat_with_drill_ai_function_success(self, mock_ai_service):
        """Test global chat function success."""
        mock_ai_service.chat_with_drill_ai.return_value = {"response": "Success"}

        result = chat_with_drill_ai("session", "message")

        assert result == "Success"
        mock_ai_service.chat_with_drill_ai.assert_called_once_with("session", "message")

    @patch('services.ai.main.ai_service')
    def test_chat_with_drill_ai_function_error(self, mock_ai_service):
        """Test global chat function error handling."""
        mock_ai_service.chat_with_drill_ai.return_value = {"error": "some_error"}

        result = chat_with_drill_ai("session", "message")

        assert result == "Error processing request"

    @patch('services.ai.main.ai_service')
    def test_get_drill_ai_insights_function_success(self, mock_ai_service):
        """Test global insights function success."""
        mock_ai_service.get_drilling_insights.return_value = {"insights": "Test insights"}

        result = get_drill_ai_insights("session")

        assert result == "Test insights"
        mock_ai_service.get_drilling_insights.assert_called_once_with("session")

    @patch('services.ai.main.ai_service')
    def test_get_drill_ai_insights_function_error(self, mock_ai_service):
        """Test global insights function error handling."""
        mock_ai_service.get_drilling_insights.return_value = {"error": "some_error"}

        result = get_drill_ai_insights("session")

        assert result == "Error getting insights"


class TestHelperFunctions:
    """Test cases for helper functions."""

    @pytest.mark.parametrize("error_type,error_detail,expected", [
        ("invalid_session", "", ERROR_MESSAGES["invalid_session"]),
        ("processing_error", "Test error", "I apologize, but I encountered an error processing your request: Test error"),
        ("no_response", "", ERROR_MESSAGES["no_response"]),
    ])
    def test_create_error_response(self, error_type, error_detail, expected):
        """Test create_error_response function."""
        from ..main import create_error_response

        result = create_error_response("session_id", error_type, error_detail)

        assert result["response"] == expected
        assert result["error"] == error_type
        assert result["session_id"] == "session_id"

    def test_create_success_response(self):
        """Test create_success_response function."""
        from ..main import create_success_response

        with patch('services.ai.main.ai_settings') as mock_settings:
            mock_settings.model_provider = "test_provider"

            result = create_success_response("Test response", "session_id")

            assert result["response"] == "Test response"
            assert result["session_id"] == "session_id"
            assert result["agent"] == "drill_agent"
            assert result["model_provider"] == "test_provider"
