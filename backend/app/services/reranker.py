from sentence_transformers import CrossEncoder

from app.core.logger import logger


model = CrossEncoder(
    "BAAI/bge-reranker-v2-m3"
)


def rerank(
    question,
    documents,
    top_k=3
):

    logger.info(
        "Reranking started"
    )

    logger.info(
        f"Reranking candidates: {len(documents)}"
    )

    pairs = []

    for doc in documents:

        pairs.append(
            [
                question,
                doc["content"]
            ]
        )

    scores = model.predict(
        pairs
    )

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for doc, score in ranked[:top_k]:

        doc["rerank_score"] = float(score)

        results.append(doc)

    logger.info(
        f"Reranking completed. "
        f"Top results: {len(results)}"
    )

    return results