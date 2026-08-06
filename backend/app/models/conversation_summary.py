from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class ConversationSummary(Base):

    __tablename__ = "conversation_summaries"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False
    )


    summary = Column(
        Text,
        nullable=False
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )