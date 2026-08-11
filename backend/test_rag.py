import pytest

from app.core.database import SessionLocal
from app.models.conversation import Conversation
from app.services.rag import ask_question


def test_rag_direct_question():

    db = SessionLocal()

    try:

        conversation = Conversation(
            user_id=1,
            title="RAG Test"
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        response = ask_question(

            db=db,

            question="How many annual leave days do employees receive?",

            conversation_id=conversation.id,

            user_id=1

        )

        assert response is not None

        assert "answer" in response

        assert "sources" in response

        assert response["answer"]

        assert isinstance(
            response["sources"],
            list
        )

    finally:

        db.close()