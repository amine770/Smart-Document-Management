from sqlalchemy import Enum, Column, Integer, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime
import enum

class FileType(str, enum.Enum):
    pdf = "pdf",
    jpg = "jpg",
    png = "png",
    txt = "txt",
    docx = "docx",
    jpeg = "jpeg"

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(Enum(FileType), nullable=False)
    size_bytes = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, 
                        onupdate=datetime.utcnow,
                        nullable=False)
    
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=True)

    uploader = relationship("User", back_populates="documents")
    folder = relationship("Folder", back_populates="documents")
    extracted_text = relationship("ExtractedText", 
                                  back_populates="document",
                                  uselist=False, # for one to one
                                  cascade="all, delete-orphan")
    
    tags = relationship("Tag",
                        secondary="document_tags", # for many to many
                        back_populates="documents")
    
    def __repr__(self):
        return f"<Document(id={self.id}, title={self.title}, type={self.file_type})"



