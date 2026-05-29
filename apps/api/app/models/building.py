from datetime import date
from typing import Any

from sqlalchemy import Date, ForeignKey, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class Building(IdMixin, TimestampMixin, Base):
    __tablename__ = "buildings"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    parcel_id: Mapped[str | None] = mapped_column(ForeignKey("parcels.id"), index=True)
    registry_pk: Mapped[str | None] = mapped_column(String(80), index=True)
    name: Mapped[str | None] = mapped_column(String(200))
    main_use: Mapped[str | None] = mapped_column(String(120))
    building_area: Mapped[float | None] = mapped_column(Numeric(14, 2))
    total_floor_area: Mapped[float | None] = mapped_column(Numeric(14, 2))
    floor_count_above: Mapped[int | None]
    floor_count_under: Mapped[int | None]
    approval_date: Mapped[date | None] = mapped_column(Date)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    project: Mapped["Project"] = relationship(back_populates="buildings")
    parcel: Mapped["Parcel | None"] = relationship(back_populates="buildings")
