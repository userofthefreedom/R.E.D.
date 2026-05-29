from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class RuleExecutionTrace(IdMixin, TimestampMixin, Base):
    __tablename__ = "rule_execution_traces"

    run_id: Mapped[str] = mapped_column(ForeignKey("diagnosis_runs.id"), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(120), nullable=False)
    rule_name: Mapped[str] = mapped_column(String(200), nullable=False)
    input_fields: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    result: Mapped[str] = mapped_column(String(120), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)

    run: Mapped["DiagnosisRun"] = relationship(back_populates="rule_traces")
