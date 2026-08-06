from app.core.database import SessionLocal

from app.services.chat_memory import (
    create_conversation,
    save_message,
    get_history
)



db = SessionLocal()


conversation = create_conversation(
    db=db,
    user_id=1
)


print(
    "Conversation ID:",
    conversation.id
)



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
    conversation_id=conversation.id
)


for message in history:

    print(
        message.role,
        ":",
        message.content
    )


db.close()