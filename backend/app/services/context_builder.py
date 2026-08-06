from app.services.chat_memory import get_history
from app.services.memory import get_summary



def build_context(
    db,
    conversation_id: int,
    user_id: int
):


    summary = get_summary(

        db=db,

        conversation_id=conversation_id

    )


    history_messages = get_history(

        db=db,

        conversation_id=conversation_id,

        user_id=user_id

    )


    history = "\n".join(

        [

            f"{msg.role}: {msg.content}"

            for msg in history_messages

        ]

    )


    context = f"""

Conversation summary:

{summary}


Recent conversation:

{history}

"""


    return context