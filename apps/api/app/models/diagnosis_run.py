from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class DiagnosisRun(IdMixin, TimestampMixin, Base):
    __tablename__ = "diagnosis_runs"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    action_id: Mapped[str | None] = mapped_column(ForeignKey("actions.id"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="pending", nullable=False)
    rule_set_version: Mapped[str | None] = mapped_column(String(80))
    rag_index_version: Mapped[str | None] = mapped_column(String(80))
    data_base_date: Mapped[str | None] = mapped_column(String(20))
    law_base_date: Mapped[str | None] = mapped_column(String(20))
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    project: Mapped["Project"] = relationship(back_populates="diagnosis_runs")
    action: Mapped["Action | None"] = relationship(back_populates="diagnosis_runs")
    result: Mapped["DiagnosisResult | None"] = relationship(back_populates="run", cascade="all, delete-orphan")
    procedure_results: Mapped[list["ProcedureResult"]] = relationship(back_populates="run", cascade="all, delete-orphan")
    evidence_traces: Mapped[list["EvidenceTrace"]] = relationship(back_populates="run", cascade="all, delete-orphan")
    rule_traces: Mapped[list["RuleExecutionTrace"]] = relationship(back_populates="run", cascade="all, delete-orphan")
