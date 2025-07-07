from fastapi import Depends
from app.services.nlp_service import NLPService
from app.services.rag_service import RAGService
import logging

logger = logging.getLogger("nlp_pipeline")

async def init_services():
    """Initialize services to ensure connections are ready."""
    try:
        # Initialize NLPService
        nlp_service = NLPService()
        # Test Redis connection
        await nlp_service.redis.ping()
        logger.info("NLPService initialized successfully with Redis connection.")

        # Initialize RAGService
        rag_service = RAGService()
        # Test Weaviate connection by querying schema
        rag_service.vector_store.client.schema.get()
        logger.info("RAGService initialized successfully with Weaviate connection.")
    except Exception as e:
        logger.error(f"Service initialization failed: {str(e)}")
        raise

def get_nlp_service() -> NLPService:
    """Dependency for NLPService."""
    return NLPService()

def get_rag_service() -> RAGService:
    """Dependency for RAGService."""
    return RAGService()