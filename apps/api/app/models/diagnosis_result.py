from typing import Any

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class DiagnosisResult(IdMixin, TimestampMixin, Base):
    __tablename__ = "diagnosis_results"

    run_id: Mapped[str] = mapped_column(ForeignKey("diagnosis_runs.id"), nullable=False, unique=True)
    overall: Mapped[str] = mapped_column(String(80), nullable=False)
    main_permit_type: Mapped[str | None] = mapped_column(String(120))
    risk_level: Mapped[str | None] = mapped_column(String(40))
    missing_info_count: Mapped[int] = mapped_column(default=0, nullable=False)
    required_actions: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    summary_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    run: Mapped["DiagnosisRun"] = relationship(back_populates="result")
