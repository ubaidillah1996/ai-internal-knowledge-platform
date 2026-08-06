from pydantic import BaseModel
from typing import List



class ChatRequest(BaseModel):

    conversation_id: int

    query: str



class Source(BaseModel):

    filename: str | None = None

    chunks: List[int]

    best_distance: float



class ChatResponse(BaseModel):

    answer: str

    sources: List[Source]

from datetime import datetime


class MessageResponse(BaseModel):

    id: int

    role: str

    content: str

    created_at: datetime


    class Config:

        from_attributes = True