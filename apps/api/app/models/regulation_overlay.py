from datetime import date, datetime
from typing import Any

from sqlalchemy import Date, DateTime, ForeignKey, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class RegulationOverlay(IdMixin, TimestampMixin, Base):
    __tablename__ = "regulation_overlays"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    parcel_id: Mapped[str | None] = mapped_column(ForeignKey("parcels.id"), index=True)
    layer_code: Mapped[str | None] = mapped_column(String(80), index=True)
    layer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    regulation_type: Mapped[str | None] = mapped_column(String(80))
    jurisdiction: Mapped[str | None] = mapped_column(String(120))
    overlap_area: Mapped[float | None] = mapped_column(Numeric(14, 2))
    overlap_ratio: Mapped[float | None] = mapped_column(Numeric(8, 5))
    source_name: Mapped[str | None] = mapped_column(String(120))
    source_url: Mapped[str | None] = mapped_column(String(500))
    data_base_date: Mapped[date | None] = mapped_column(Date)
    collected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    project: Mapped["Project"] = relationship(back_populates="regulation_overlays")
    parcel: Mapped["Parcel | None"] = relationship(back_populates="regulation_overlays")
