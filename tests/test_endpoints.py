from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_classify_endpoint():
    response = client.post("/api/v1/classify", json={"text": "Test text", "webhook_url": None})
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert response.json()["status"] == "queued"

def test_extract_endpoint():
    response = client.post("/api/v1/extract", json={"text": "Test text", "webhook_url": None})
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert response.json()["status"] == "queued"

def test_summarize_endpoint():
    response = client.post("/api/v1/summarize", json={"text": "Test text", "webhook_url": None})
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert response.json()["status"] == "queued"

def test_sentiment_endpoint():
    response = client.post("/api/v1/sentiment", json={"text": "Test text", "webhook_url": None})
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert response.json()["status"] == "queued"

def test_batch_endpoint():
    response = client.post("/api/v1/batch", json={"texts": ["Text1", "Text2"], "webhook_url": None})
    assert response.status_code == 200
    assert "task_id" in response.json()
    assert response.json()["status"] == "queued"

def test_retrieve_endpoint():
    response = client.post("/api/v1/retrieve", json={"text": "Test query", "webhook_url": None})
    assert response.status_code == 200
    assert "results" in response.json()