from app.services.embedding import create_embedding
from app.services.vector_store import search_embedding


def test_vector_search():

    query = "Who approves annual leave?"

    embedding = create_embedding(query)

    results = search_embedding(

        embedding,

        limit=5,

        threshold=1.0

    )

    assert results is not None

    assert isinstance(
        results,
        list
    )

    for item in results:

        assert "content" in item

        assert "metadata" in item

        assert "distance" in item