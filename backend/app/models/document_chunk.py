from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.core.database import Base
from sqlalchemy.orm import relationship

class DocumentChunk(Base):

    __tablename__ = "document_chunks"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False
    )


    content = Column(
        Text,
        nullable=False
    )


    chunk_index = Column(
        Integer,
        nullable=False
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    document = relationship(
    "Document",
    back_populates="chunks"
    )