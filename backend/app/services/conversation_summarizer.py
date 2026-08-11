from app.core.logger import logger
import ollama

from app.core.config import settings
from app.models.conversation import Conversation



def generate_summary(history: str):

    prompt = f"""
Summarize the following conversation.

Rules:

- Preserve important facts.
- Preserve decisions.
- Preserve policies mentioned.
- Preserve names and responsibilities.
- Keep summary under 200 words.

Conversation:

{history}

Summary:
"""

    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        options={
            "temperature": 0
        },
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    summary = (
        response["message"]["content"]
        .strip()
    )

    logger.info(
        "Conversation summary generated"
    )

    return summary



def save_summary(
    db,
    conversation_id,
    summary,
    message_count
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id
        )
        .first()
    )

    if not conversation:
        return

    conversation.summary = summary

    conversation.summary_message_count = (
        message_count
    )

    db.commit()

