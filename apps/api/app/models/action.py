from typing import Any

from sqlalchemy import ForeignKey, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class Action(IdMixin, TimestampMixin, Base):
    __tablename__ = "actions"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(40), nullable=False)
    current_use: Mapped[str | None] = mapped_column(String(120))
    desired_use: Mapped[str | None] = mapped_column(String(120))
    site_area: Mapped[float | None] = mapped_column(Numeric(14, 2))
    building_area: Mapped[float | None] = mapped_column(Numeric(14, 2))
    total_floor_area: Mapped[float | None] = mapped_column(Numeric(14, 2))
    floor_count_above: Mapped[int | None]
    floor_count_under: Mapped[int | None]
    parking_before: Mapped[int | None]
    parking_after: Mapped[int | None]
    site_conditions: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    construction_method: Mapped[str | None] = mapped_column(String(120))
    business_purpose: Mapped[str | None] = mapped_column(String(300))
    memo: Mapped[str | None] = mapped_column(Text)
    normalized_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    project: Mapped["Project"] = relationship(back_populates="actions")
    diagnosis_runs: Mapped[list["DiagnosisRun"]] = relationship(back_populates="action")
