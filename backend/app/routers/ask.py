from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.services.rag import ask_question

from app.core.auth import get_current_user

from app.models.user import User

from app.schemas.chat import ChatRequest, ChatResponse

from app.core.database import get_db

from app.models.conversation import Conversation
from fastapi import HTTPException

router = APIRouter(

    prefix="/ask",

    tags=["AI Assistant"]

)



@router.post("/", response_model=ChatResponse)
def ask_ai(

    request: ChatRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
 
):

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == current_user.id
        )
        .first()
    )


    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    


    result = ask_question(

        db=db,

        question=request.query,

        conversation_id=request.conversation_id,

        user_id=current_user.id

    )


    return {

    "answer": result["answer"],

    "sources": result["sources"]

}