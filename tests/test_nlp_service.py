from fastapi.testclient import TestClient
from app.main import app
from app.services.nlp_service import NLPService
from app.mlflow.tracking import log_model_metrics
from unittest.mock import AsyncMock, patch
import pytest
import asyncio
import time

@pytest.fixture
def nlp_service():
    return NLPService()

@pytest.mark.asyncio
async def test_process_text_classify(nlp_service):
    with patch.object(nlp_service.client.chat.completions, "create", new=AsyncMock(return_value=MockCompletion())):
        start_time = time.time()
        result = await nlp_service.process_text("I love this product!", "classify")
        execution_time = time.time() - start_time
        log_model_metrics("classify", {"accuracy": 1.0}, execution_time)
        assert result == "positive"

@pytest.mark.asyncio
async def test_process_text_extract(nlp_service):
    with patch.object(nlp_service.client.chat.completions, "create", new=AsyncMock(return_value=MockCompletion(content="Entities: [Apple:ORG, Steve Jobs:PERSON]"))):
        start_time = time.time()
        result = await nlp_service.process_text("Apple was founded by Steve Jobs.", "extract")
        execution_time = time.time() - start_time
        log_model_metrics("extract", {"entity_count": 2}, execution_time)
        assert "Apple:ORG" in result

@pytest.mark.asyncio
async def test_process_batch(nlp_service):
    with patch.object(nlp_service.client.chat.completions, "create", new=AsyncMock(return_value=MockCompletion())):
        start_time = time.time()
        results = await nlp_service.process_batch(["Text1", "Text2"], "classify")
        execution_time = time.time() - start_time
        log_model_metrics("batch", {"batch_size": 2}, execution_time)
        assert len(results) == 2
        assert all(result == "positive" for result in results)

@pytest.mark.asyncio
async def test_cache_hit(nlp_service):
    with patch.object(nlp_service.redis, "get", new=AsyncMock(return_value=b"cached_result")):
        result = await nlp_service.process_text("Test text", "classify")
        assert result == "cached_result"
        nlp_service.client.chat.completions.create.assert_not_called()

class MockCompletion:
    def __init__(self, content="positive"):
        self.choices = [type('Choice', (), {'message': type('Message', (), {'content': content})})()]