from langchain.vectorstores import Weaviate
from langchain.embeddings.openai import OpenAIEmbeddings
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from app.core.config import settings
from app.utils.reranker import rerank_results
import logging

logger = logging.getLogger("nlp_pipeline")

class RAGState(TypedDict):
    query: str
    documents: List[str]
    top_k: int

class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.API_KEY,
            model=settings.EMBEDDING_MODEL,
            base_url=settings.ULTRASAFE_API_URL,
        )
        self.vector_store = Weaviate(
            weaviate_url=settings.WEAVIATE_URL,
            index_name="Documents",
            text_key="content",
            embedding=self.embeddings,
        )
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build a LangGraph workflow for RAG."""
        graph = StateGraph(RAGState)

        graph.add_node("retrieve", self._retrieve_node)
        graph.add_node("rerank", self._rerank_node)

        graph.add_edge("retrieve", "rerank")
        graph.add_edge("rerank", END)

        graph.set_entry_point("retrieve")
        return graph.compile()

    def _retrieve_node(self, state: RAGState) -> RAGState:
        """Retrieve documents from vector store."""
        query_embedding = self.embeddings.embed_query(state["query"])
        results = self.vector_store.similarity_search_by_vector(query_embedding, k=state["top_k"] * 2)
        state["documents"] = [doc.page_content for doc in results]
        logger.info(f"Retrieved {len(state['documents'])} documents for query: {state['query'][:50]}...")
        return state

    def _rerank_node(self, state: RAGState) -> RAGState:
        """Rerank retrieved documents."""
        state["documents"] = rerank_results(state["query"], state["documents"])[:state["top_k"]]
        logger.info(f"Reranked to {len(state['documents'])} documents.")
        return state

    async def retrieve_similar(self, query: str, top_k: int = 5) -> list:
        """Execute the RAG workflow."""
        try:
            state = await self.graph.ainvoke({"query": query, "top_k": top_k, "documents": []})
            return state["documents"]
        except Exception as e:
            logger.error(f"RAG retrieval failed: {str(e)}")
            raise