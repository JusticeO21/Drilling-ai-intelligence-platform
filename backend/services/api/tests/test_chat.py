import pytest
from fastapi.testclient import TestClient
from ..app.main import app

client = TestClient(app)


def test_chat_endpoint_invalid_session():
    """Test chat with invalid session returns error"""
    response = client.post(
        "/api/v1/chat/", json={"session_id": "invalid-session", "message": "Hello"}
    )

    assert response.status_code == 200  # AI service handles session validation
    data = response.json()
    assert "error" in data["response"].lower() or "expired" in data["response"].lower()


def test_chat_endpoint_structure():
    """Test chat endpoint returns proper structure"""
    response = client.post(
        "/api/v1/chat/",
        json={"session_id": "test-session", "message": "What is the depth?"},
    )

    assert response.status_code == 200
    data = response.json()

    required_fields = ["response", "session_id", "model_provider", "processing_time"]
    for field in required_fields:
        assert field in data

    assert data["session_id"] == "test-session"
    assert isinstance(data["processing_time"], (int, float))


def test_chat_endpoint_with_history():
    """Test chat endpoint with conversation history"""
    chat_history = [
        {"user": "Hello", "assistant": "Hi there!"},
        {"user": "How are you?", "assistant": "I'm doing well, thank you!"},
    ]

    response = client.post(
        "/api/v1/chat/",
        json={
            "session_id": "test-session",
            "message": "What's the weather like?",
            "chat_history": chat_history,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["session_id"] == "test-session"
