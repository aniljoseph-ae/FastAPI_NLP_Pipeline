from sentence_transformers import CrossEncoder
import logging

logger = logging.getLogger("nlp_pipeline")

def rerank_results(query: str, documents: list) -> list:  # Renamed for consistency
    try:
        model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        pairs = [[query, doc] for doc in documents]
        scores = model.predict(pairs)
        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )
        logger.info(f"Reranked {len(documents)} documents for query: {query[:50]}...")
        return [doc for doc, _ in ranked]
    except Exception as e:
        logger.error(f"Reranking failed: {str(e)}")
        raise
       