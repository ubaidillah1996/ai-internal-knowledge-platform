import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.core.logger import logger

from app.models.user import User
from app.models.conversation import Conversation

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.services.rag import ask_question


router = APIRouter(

    prefix="/ask",

    tags=["AI Assistant"]

)



@router.post(
    "/",
    response_model=ChatResponse
)
def ask_ai(

    request: ChatRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):


    request_id = str(uuid.uuid4())[:8]


    logger.info(
        f"[{request_id}] AI request started"
    )


    logger.info(
        f"[{request_id}] User ID: {current_user.id}"
    )


    logger.info(
        f"[{request_id}] Conversation ID: {request.conversation_id}"
    )


    logger.info(
        f"[{request_id}] Question: {request.query}"
    )



    conversation = (

        db.query(Conversation)

        .filter(

            Conversation.id == request.conversation_id,

            Conversation.user_id == current_user.id

        )

        .first()

    )



    if not conversation:


        logger.warning(

            f"[{request_id}] Conversation not found"

        )


        raise HTTPException(

            status_code=404,

            detail="Conversation not found"

        )



    try:


        result = ask_question(

            db=db,

            question=request.query,

            conversation_id=request.conversation_id,

            user_id=current_user.id

        )



        logger.info(

            f"[{request_id}] AI request completed"

        )



        return {


            "answer": result["answer"],


            "sources": result["sources"]

        }



    except Exception as e:


        logger.error(

            f"[{request_id}] AI request failed: {e}"

        )


        raise