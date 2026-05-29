from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class EvidenceTrace(IdMixin, TimestampMixin, Base):
    __tablename__ = "evidence_traces"

    run_id: Mapped[str] = mapped_column(ForeignKey("diagnosis_runs.id"), nullable=False, index=True)
    chunk_id: Mapped[str | None] = mapped_column(ForeignKey("evidence_chunks.id"), index=True)
    procedure_name: Mapped[str] = mapped_column(String(120), nullable=False)
    source_title: Mapped[str] = mapped_column(String(300), nullable=False)
    source_chunk_id: Mapped[str | None] = mapped_column(String(120))
    reason: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[float | None] = mapped_column(Float)

    run: Mapped["DiagnosisRun"] = relationship(back_populates="evidence_traces")
    chunk: Mapped["EvidenceChunk | None"] = relationship(back_populates="evidence_traces")
