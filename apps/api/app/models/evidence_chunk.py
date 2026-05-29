from typing import Any

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class EvidenceChunk(IdMixin, TimestampMixin, Base):
    __tablename__ = "evidence_chunks"

    document_id: Mapped[str] = mapped_column(ForeignKey("legal_documents.id"), nullable=False, index=True)
    chunk_id: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    heading: Mapped[str | None] = mapped_column(String(300))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    article_no: Mapped[str | None] = mapped_column(String(80))
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    embedding_model: Mapped[str | None] = mapped_column(String(80))
    index_version: Mapped[str | None] = mapped_column(String(80))

    document: Mapped["LegalDocument"] = relationship(back_populates="chunks")
    evidence_traces: Mapped[list["EvidenceTrace"]] = relationship(back_populates="chunk")
