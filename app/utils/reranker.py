from sentence_transformers import CrossEncoder


def reranker_result(query: str, documents: list) -> list:
    model = CrossEncoder("cross-encoder/ms-macro-MiniLM-L-6-v2")
    pairs = [[query, doc] for doc in documents]
    scores = model.predict(pairs)
    ranked = sorted(
        zip(documents, scores), 
        key = lambda x : x[1], 
        reverse = True
    )

    return [doc for doc, _ in ranked]