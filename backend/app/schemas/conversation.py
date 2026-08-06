from pydantic import BaseModel
from datetime import datetime
from typing import List 

class ConversationCreate(BaseModel):
    pass



class ConversationResponse(BaseModel):

    id:int

    title:str

    created_at:datetime


    class Config:
        from_attributes=True

class ConversationListResponse(BaseModel):

    total: int

    data: List[ConversationResponse]