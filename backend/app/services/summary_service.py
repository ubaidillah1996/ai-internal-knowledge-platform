from sqlalchemy.orm import Session

from app.models.conversation_summary import ConversationSummary


def get_summary(
    db: Session,
    conversation_id: int
):

    summary = (

        db.query(
            ConversationSummary
        )

        .filter(
            ConversationSummary.conversation_id == conversation_id
        )

        .first()

    )


    if not summary:
        return None


    return summary.summary

def save_summary(
    db: Session,
    conversation_id: int,
    summary_text: str
):


    existing = (

        db.query(
            ConversationSummary
        )

        .filter(
            ConversationSummary.conversation_id == conversation_id
        )

        .first()

    )


    if existing:

        existing.summary = summary_text


    else:

        new_summary = ConversationSummary(

            conversation_id=conversation_id,

            summary=summary_text

        )

        db.add(new_summary)


    db.commit()