from datetime import date, datetime
from typing import Any

from sqlalchemy import Date, DateTime, ForeignKey, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class Parcel(IdMixin, TimestampMixin, Base):
    __tablename__ = "parcels"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    pnu: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    standard_address: Mapped[str | None] = mapped_column(String(300))
    jibun_address: Mapped[str | None] = mapped_column(String(300))
    legal_dong_code: Mapped[str | None] = mapped_column(String(20))
    land_category: Mapped[str | None] = mapped_column(String(40))
    site_area: Mapped[float | None] = mapped_column(Numeric(14, 2))
    use_district: Mapped[str | None] = mapped_column(String(120))
    district_unit_plan: Mapped[bool] = mapped_column(default=False, nullable=False)
    geometry_geojson: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    data_base_date: Mapped[date | None] = mapped_column(Date)
    collected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    project: Mapped["Project"] = relationship(back_populates="parcels")
    buildings: Mapped[list["Building"]] = relationship(back_populates="parcel")
    regulation_overlays: Mapped[list["RegulationOverlay"]] = relationship(back_populates="parcel", cascade="all, delete-orphan")
