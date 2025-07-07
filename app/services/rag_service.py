from langchain.vectorstores import Weaviate
from langchain.embeddings.openai import OpenAIEmbeddings

from app.core.config import settings
from app.utils.reranker import reranker_result

class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.API_KEY,
            model=settings.EMBEDDING_MODEL,
            base_url=settings.ULTRASAFE_API_URL
        )

        self.vector_store = Weaviate(
            weaviate_url=settings.WEAVIATE_URL,
            index_name="Documents",
            text_key="content",
            embedding=self.embeddings,
        )
    async def retrieve_similar(self, query: str, top_k: int =5) -> list:
        # generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # retrieve from vector store
        results = self.vector_store.similarity_search_by_vector(query_embedding, k=top_k * 2) 
        # rerank result
        reranked = reranker_result(
            query,
            [doc.page_content for doc in results]
        )
        return reranked[ : top_k]