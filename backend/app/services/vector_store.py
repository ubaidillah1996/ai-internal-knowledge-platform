import chromadb
from torch import threshold

from app.core.config import settings
from app.core.logger import logger

client = chromadb.PersistentClient(
    path=settings.CHROMA_PATH
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
    threshold: float = 1.4
):

    logger.info(
        "Vector search started"
    )

    logger.info(
        f"Search limit: {limit}, threshold: {threshold}"
    )

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=limit

    )

    logger.info(
        f"Retrieved {len(results['documents'][0])} chunks from Chroma"
    )


    logger.info(
        f"Vector distances: {results['distances']}"
    )
    logger.info(
        f"Retrieved metadata: {results['metadatas']}"
    )


    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    distances = results["distances"][0]


    output = []


    for index, document in enumerate(documents):

        distance = distances[index]

        filename = metadatas[index].get(
            "filename",
            "Unknown"
        )

        print(
            f"Distance: {distance} | File: {filename}"
        )

    for index, document in enumerate(documents):

        distance = distances[index]


        if distance <= threshold:

            print("\n========== CHUNK ==========")
            print(document)
            print("===========================\n")
            
            output.append({

                "content": document,

                "metadata": metadatas[index],

                "distance": distance

            })


    logger.info(
        f"Relevant chunks after filtering: {len(output)}"
    )

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