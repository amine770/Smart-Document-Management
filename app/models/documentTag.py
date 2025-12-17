from sqlalchemy import ForeignKey, Column, Integer, Table, DateTime
from datetime import datetime
from app.models.base import Base

document_tags = Table(
    "document_tags",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("document_id", Integer, ForeignKey("documents.id", ondelete="cascade"), nullable=False),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="cascade"), nullable=False),
    Column("created_at",DateTime, default=datetime.utcnow, nullable=False)
)
