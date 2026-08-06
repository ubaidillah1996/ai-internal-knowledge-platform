from app.services.embedding import create_embedding
from app.services.vector_store import store_embedding


text = """
Employees receive 18 days annual leave per year.
Leave applications must be approved by managers.
"""


vector = create_embedding(text)


print("Vector dimension:", len(vector))


store_embedding(

    chunk_id=2,

    embedding=vector,

    text=text,

    metadata={
        "document_id":1
    }

)


print("Real embedding stored 🔥")