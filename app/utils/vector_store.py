from langchain.vectorstores import Weaviate
from langchain.docstore.document import Document

from app.core.config import settings
from app.utils.embedding import generate_embedding

class VectorStore:
    def __init__(self):
        self.vector_store = Weaviate(
            Weaviate_url = settings.WEAVIATE_URL,
            index_name = "Documents",
            text_key = "content",
            embedding = generate_embedding
        )

    def add_documnet(self, texts:str, metadata: list):
        documents = [Document(page_content=text, metadata=metadata) for text, metadata in zip(texts, metadata)]
        self.vector_store.add_documents(documents)