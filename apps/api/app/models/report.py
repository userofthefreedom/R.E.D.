from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class Report(IdMixin, TimestampMixin, Base):
    __tablename__ = "reports"

    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    diagnosis_run_id: Mapped[str | None] = mapped_column(ForeignKey("diagnosis_runs.id"), index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[str] = mapped_column(String(40), default="v1.0", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="draft", nullable=False)
    report_type: Mapped[str] = mapped_column(String(80), default="summary", nullable=False)
    file_path: Mapped[str | None] = mapped_column(String(500))
    content_json: Mapped[dict | None] = mapped_column(JSON)
    disclaimer: Mapped[str | None] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="reports")
