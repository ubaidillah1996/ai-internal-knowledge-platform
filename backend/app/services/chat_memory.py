from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.conversation import Conversation


def get_history(
    db: Session,
    conversation_id: int,
    user_id: int,
    limit: int = 10
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        .first()
    )


    if not conversation:
        return None


    messages = (

        db.query(Message)

        .filter(
            Message.conversation_id == conversation_id
        )

        .order_by(
            Message.created_at.desc()
        )

        .limit(limit)

        .all()

    )


    messages.reverse()


    return messages

def save_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str
):

    message = Message(

        conversation_id=conversation_id,

        role=role,

        content=content

    )


    db.add(message)

    db.commit()

    db.refresh(message)


    return message

def format_history(messages):

    history = ""


    for message in messages:

        history += (
            f"{message.role}: "
            f"{message.content}\n"
        )


    return history