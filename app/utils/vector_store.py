from langchain.vectorstores import Weaviate
from langchain.docstore.document import Document
from app.core.config import settings
from app.utils.embedding import generate_embedding
import logging

logger = logging.getLogger("nlp_pipeline")

class VectorStore:
    def __init__(self):
        self.vector_store = Weaviate(
            weaviate_url=settings.WEAVIATE_URL,  # Fixed capitalization
            index_name="Documents",
            text_key="content",
            embedding=generate_embedding
        )

    def add_documents(self, texts: list, metadatas: list):  # Fixed method name and parameter
        try:
            documents = [Document(page_content=text, metadata=metadata) for text, metadata in zip(texts, metadatas)]
            self.vector_store.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to vector store.")
        except Exception as e:
            logger.error(f"Failed to add documents: {str(e)}")
            raise