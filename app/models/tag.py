from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    documents = relationship("Document", secondary="document_tags", back_populates="tags")

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})"