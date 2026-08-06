from sqlalchemy.orm import Session

from app.models.conversation import Conversation



def update_conversation_title(
    db: Session,
    conversation_id: int,
    title: str
):


    conversation = (

        db.query(Conversation)

        .filter(
            Conversation.id == conversation_id
        )

        .first()

    )


    if conversation:

        conversation.title = title

        db.commit()

        db.refresh(conversation)


    return conversation

def update_title_if_empty(
    db,
    conversation_id: int,
    title: str
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


    if conversation.title == "New Conversation" or conversation.title is None:

        conversation.title = title[:50]

        db.commit()