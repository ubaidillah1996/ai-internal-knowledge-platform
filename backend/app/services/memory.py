from sqlalchemy.orm import Session

from app.models.conversation import Conversation



def get_summary(
    db: Session,
    conversation_id: int
):

    conversation = (

        db.query(Conversation)

        .filter(
            Conversation.id == conversation_id
        )

        .first()

    )


    if not conversation:

        return None


    return conversation.summary

def update_summary(
    db: Session,
    conversation_id: int,
    summary: str
):

    conversation = (

        db.query(Conversation)

        .filter(
            Conversation.id == conversation_id
        )

        .first()

    )


    if not conversation:

        return None


    conversation.summary = summary


    db.commit()

    db.refresh(conversation)


    return conversation

def get_summary_message_count(
    db,
    conversation_id
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id
        )
        .first()
    )


    if not conversation:
        return 0


    return conversation.summary_message_count or 0

def update_summary_message_count(
    db,
    conversation_id,
    count
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id
        )
        .first()
    )


    if conversation:

        conversation.summary_message_count = count

        db.commit()