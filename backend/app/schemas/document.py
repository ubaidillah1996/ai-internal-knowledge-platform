from pydantic import BaseModel
from datetime import datetime



class DocumentResponse(BaseModel):

    id: int

    title: str

    filename: str

    uploaded_by: int

    created_at: datetime

    updated_at: datetime


    class Config:

        from_attributes = True

class DocumentDetailResponse(BaseModel):

    id: int

    title: str

    filename: str

    uploaded_by: int

    total_chunks: int

    status: str

    created_at: datetime

    updated_at: datetime


    class Config:

        from_attributes = True

class DocumentListResponse(BaseModel):

    id: int

    title: str

    filename: str

    uploaded_by: int

    total_chunks: int

    status: str

    created_at: datetime