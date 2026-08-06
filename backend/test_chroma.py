import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="documents"
)


print(
    "Total vectors:",
    collection.count()
)