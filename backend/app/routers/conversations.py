from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user

from app.models.conversation import Conversation
from app.models.user import User

from app.schemas.conversation import (
    ConversationResponse,
    ConversationListResponse
)
from app.schemas.conversation import ConversationResponse

from app.models.message import Message

from app.schemas.message import MessageResponse

from fastapi import HTTPException

from pydantic import BaseModel

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)

@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )


    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    db.delete(conversation)

    db.commit()


    return {
        "message": "Conversation deleted successfully"
    }

@router.post(
    "/",
    response_model=ConversationResponse
)
def create_conversation(

    db:Session = Depends(get_db),

    current_user:User = Depends(get_current_user)

):


    conversation = Conversation(

        user_id=current_user.id,

        title="New Conversation"

    )


    db.add(conversation)

    db.commit()

    db.refresh(conversation)


    return conversation

@router.get(
    "/",
    response_model=ConversationListResponse
)
def get_conversations(

    skip: int = 0,

    limit: int = 10,

    search: str | None = None,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):


    query = (

        db.query(Conversation)

        .filter(
            Conversation.user_id == current_user.id
        )

    )


    if search:

        query = query.filter(
            Conversation.title.ilike(
                f"%{search}%"
            )
        )


    conversations = (

        query

        .order_by(
            Conversation.created_at.desc()
        )

        .offset(skip)

        .limit(limit)

        .all()

    )
    total = (
    
            db.query(Conversation)
    
            .filter(
                Conversation.user_id == current_user.id
            )
    
            .count()
    
        )


    return {

    "total": total,

    "data": conversations

}

class RenameConversationRequest(BaseModel):

    title: str

@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )

    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return conversation

@router.get("/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )

    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(
            Message.created_at.asc()
        )
        .all()
    )

    return messages

@router.patch("/{conversation_id}")
def rename_conversation(
    conversation_id: int,
    request: RenameConversationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):


    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )


    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    conversation.title = request.title


    db.commit()

    db.refresh(conversation)


    return {

        "message": "Conversation renamed successfully",

        "id": conversation.id,

        "title": conversation.title

    }

