from sqlalchemy import Column, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class ExtractedText(Base):
    __tablename__ = "extracted_text"
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="cascade"), primary_key=True)
    content = Column(Text, nullable=False)
    extarcted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    document = relationship("Document", back_populates="extracted_text")

    def __repr__(self):
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<ExtractedText(document_id={self.document_id}, preview='{content_preview}')>"