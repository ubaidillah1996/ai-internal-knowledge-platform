from sentence_transformers import CrossEncoder


model = CrossEncoder(
    "BAAI/bge-reranker-v2-m3"
)


def rerank(
    question,
    documents,
    top_k=3
):

    pairs = []


    for doc in documents:

        pairs.append(
            [
                question,
                doc["text"]
            ]
        )


    scores = model.predict(
        pairs
    )


    ranked = sorted(
        zip(documents, scores),
        key=lambda x:x[1],
        reverse=True
    )


    results=[]


    for doc, score in ranked[:top_k]:

        doc["rerank_score"] = float(score)

        results.append(doc)


    return results