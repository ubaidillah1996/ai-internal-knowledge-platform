from app.services.vector_store import collection
from app.services.embedding import create_embedding


def search_documents(
    query: str,
    limit: int = 3
):

    query_vector = create_embedding(query)


    results = collection.query(

        query_embeddings=[
            query_vector
        ],

        n_results=limit

    )


    return results