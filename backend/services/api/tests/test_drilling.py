import io
from fastapi.testclient import TestClient
from ..app.main import app

client = TestClient(app)


def test_upload_csv():
    csv_content = "well_name,depth,pressure\ntest_well,1500,200\nanother_well,2200,250"
    files = {"file": ("test.csv", io.BytesIO(csv_content.encode()), "text/csv")}
    response = client.post("/api/v1/drilling/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.csv"
    assert data["file_type"] == "csv"
    assert data["num_rows"] == 2
    assert data["num_columns"] == 3
    assert "session_id" in data
    assert "chunks_count" in data
    assert data["chunks_count"] == 2

    # Test querying the session
    session_id = data["session_id"]
    query_data = {"session_id": session_id, "question": "What is the depth of test_well?"}
    query_response = client.post("/api/v1/drilling/query", json=query_data)
    assert query_response.status_code == 200
    query_result = query_response.json()
    assert query_result["session_id"] == session_id
    assert query_result["question"] == "What is the depth of test_well?"
    assert "relevant_chunks" in query_result


def test_upload_invalid_file():
    files = {"file": ("test.txt", io.BytesIO(b"invalid"), "text/plain")}
    response = client.post("/api/v1/drilling/upload", files=files)
    assert response.status_code == 400


def test_query_invalid_session():
    query_data = {"session_id": "invalid-session-id", "question": "Test question"}
    response = client.post("/api/v1/drilling/query", json=query_data)
    assert response.status_code == 404


def test_get_session_info():
    # First create a session
    csv_content = "well_name,depth\ntest_well,1500"
    files = {"file": ("test.csv", io.BytesIO(csv_content.encode()), "text/csv")}
    upload_response = client.post("/api/v1/drilling/upload", files=files)
    session_id = upload_response.json()["session_id"]

    # Get session info
    info_response = client.get(f"/api/v1/drilling/session/{session_id}")
    assert info_response.status_code == 200
    info = info_response.json()
    assert info["session_id"] == session_id
    assert "created_at" in info
    assert "expires_at" in info


def test_get_invalid_session_info():
    response = client.get("/api/v1/drilling/session/invalid-session")
    assert response.status_code == 404
