from app.services.rag_service import RAGService
from unittest.mock import Mock, patch
import pytest
import asyncio

@pytest.fixture
def rag_service():
    return RAGService()

@pytest.mark.asyncio
async def test_retrieve_similar(rag_service):
    mock_results = [
        type('Doc', (), {'page_content': "Doc1"}),
        type('Doc', (), {'page_content': "Doc2"}),
    ]
    with patch.object(rag_service.vector_store, "similarity_search_by_vector", return_value=mock_results):
        with patch("app.utils.reranker.rerank_results", return_value=["Doc1", "Doc2"]):
            results = await rag_service.retrieve_similar("Test query", top_k=2)
            assert len(results) == 2
            assert results == ["Doc1", "Doc2"]

@pytest.mark.asyncio
async def test_embedding_generation(rag_service):
    with patch.object(rag_service.embeddings, "embed_query", return_value=[0.1, 0.2, 0.3]):
        embedding = rag_service.embeddings.embed_query("Test query")
        assert len(embedding) == 3
        assert embedding == [0.1, 0.2, 0.3]

@pytest.mark.asyncio
async def test_langgraph_workflow(rag_service):
    with patch.object(rag_service.vector_store, "similarity_search_by_vector", return_value=[
        type('Doc', (), {'page_content': "Doc1"}),
        type('Doc', (), {'page_content': "Doc2"}),
    ]):
        with patch("app.utils.reranker.rerank_results", return_value=["Doc1", "Doc2"]):
            state = await rag_service.graph.ainvoke({"query": "Test query", "top_k": 2, "documents": []})
            assert state["documents"] == ["Doc1", "Doc2"]