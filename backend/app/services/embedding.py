from sentence_transformers import SentenceTransformer

from app.core.logger import logger


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embedding(text: str):

    logger.info(
        "Creating embedding..."
    )


    logger.info(
        f"Embedding input length: {len(text)} characters"
    )


    embedding = model.encode(text)


    logger.info(
        "Embedding created successfully"
    )


    return embedding.tolist()