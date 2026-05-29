from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class ProcedureResult(IdMixin, TimestampMixin, Base):
    __tablename__ = "procedure_results"

    run_id: Mapped[str] = mapped_column(ForeignKey("diagnosis_runs.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    target: Mapped[str] = mapped_column(String(40), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    department: Mapped[str | None] = mapped_column(String(120))
    risk: Mapped[str | None] = mapped_column(String(40))
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)

    run: Mapped["DiagnosisRun"] = relationship(back_populates="procedure_results")
    required_documents: Mapped[list["RequiredDocument"]] = relationship(back_populates="procedure", cascade="all, delete-orphan")
