import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="documents"
)


def store_embedding(
    chunk_id: int,
    embedding: list,
    text: str,
    metadata: dict
):

    print(
        "STORE EMBEDDING TEXT TYPE:",
        type(text)
    )

    collection.add(

        ids=[
            str(chunk_id)
        ],

        embeddings=[
            embedding
        ],

        documents=[
            text
        ],

        metadatas=[
            metadata
        ]
    )

def search_embedding(
    query_embedding: list,
    limit: int = 5,
    threshold: float = 1.0
):

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=limit

    )


    print(results["distances"])
    print(results["metadatas"])


    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]


    output = []


    for index, document in enumerate(documents):

        distance = distances[index]


        if distance <= threshold:

            output.append({

                "content": document,

                "metadata": metadatas[index],

                "distance": distance

            })


    return output

def delete_embedding(
    chunk_ids: list
):

    print(
        "DELETING FROM CHROMA:",
        chunk_ids
    )

    collection.delete(

        ids=[
            str(chunk_id)
            for chunk_id in chunk_ids
        ]

    )