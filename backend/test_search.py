from app.services.embedding import create_embedding
from app.services.vector_store import search_embedding


query = "Who approves annual leave?"


embedding = create_embedding(query)


results = search_embedding(
    embedding,
    limit=5,
    threshold=1.0
)


for item in results:

    print("================")

    print(item["metadata"])

    print(item["content"])
    
    print(item["distance"])