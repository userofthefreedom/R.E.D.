from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class Project(IdMixin, TimestampMixin, Base):
    __tablename__ = "projects"

    owner_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="draft", nullable=False)
    risk_level: Mapped[str | None] = mapped_column(String(40))
    address: Mapped[str | None] = mapped_column(String(300))
    pnu: Mapped[str | None] = mapped_column(String(32), index=True)
    description: Mapped[str | None] = mapped_column(Text)

    owner: Mapped["User | None"] = relationship(back_populates="projects")
    parcels: Mapped[list["Parcel"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    buildings: Mapped[list["Building"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    regulation_overlays: Mapped[list["RegulationOverlay"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    actions: Mapped[list["Action"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    diagnosis_runs: Mapped[list["DiagnosisRun"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    reports: Mapped[list["Report"]] = relationship(back_populates="project", cascade="all, delete-orphan")
