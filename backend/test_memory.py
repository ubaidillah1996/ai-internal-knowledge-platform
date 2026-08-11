from app.core.database import SessionLocal
from app.models.conversation import Conversation

from app.services.chat_memory import (
    save_message,
    get_history
)


def test_conversation_memory():

    db = SessionLocal()

    try:

        conversation = Conversation(

            user_id=1,

            title="Memory Test"

        )

        db.add(conversation)

        db.commit()

        db.refresh(conversation)

        save_message(

            db=db,

            conversation_id=conversation.id,

            role="user",

            content="How many annual leave days?"

        )

        save_message(

            db=db,

            conversation_id=conversation.id,

            role="assistant",

            content="Employees receive 18 days annual leave."

        )

        history = get_history(

            db=db,

            conversation_id=conversation.id,

            user_id=1

        )

        assert history is not None

        assert len(history) == 2

        assert history[0].role == "user"

        assert history[1].role == "assistant"

        assert history[0].content == (
            "How many annual leave days?"
        )

        assert history[1].content == (
            "Employees receive 18 days annual leave."
        )

    finally:

        db.close()