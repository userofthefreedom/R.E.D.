from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class LegalDocument(IdMixin, TimestampMixin, Base):
    __tablename__ = "legal_documents"

    source_code: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    jurisdiction: Mapped[str | None] = mapped_column(String(120))
    document_type: Mapped[str | None] = mapped_column(String(80))
    effective_date: Mapped[date | None] = mapped_column(Date)
    collected_date: Mapped[date | None] = mapped_column(Date)
    source_url: Mapped[str | None] = mapped_column(String(500))

    chunks: Mapped[list["EvidenceChunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")
