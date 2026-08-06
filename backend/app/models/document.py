from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Document(Base):

    __tablename__ = "documents"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(
        String,
        nullable=False
    )


    filename = Column(
        String,
        nullable=False
    )


    file_path = Column(
        String,
        nullable=False
    )


    content = Column(
        Text,
        nullable=True
    )


    uploaded_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )   

    chunks = relationship(
    "DocumentChunk",
    back_populates="document",
    cascade="all, delete-orphan"
    )