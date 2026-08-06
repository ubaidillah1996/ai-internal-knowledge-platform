import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_collection(
    name="documents"
)


result = collection.get()


print("IDs:")
print(result["ids"])


print("\nMetadata:")

for meta in result["metadatas"]:
    print(meta)

result = collection.get(
    ids=["35"],
    include=[
        "documents",
        "embeddings",
        "metadatas"
    ]
)

print(result)