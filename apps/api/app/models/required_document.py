from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class RequiredDocument(IdMixin, TimestampMixin, Base):
    __tablename__ = "required_documents"

    procedure_id: Mapped[str] = mapped_column(ForeignKey("procedure_results.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(200))
    is_optional: Mapped[bool] = mapped_column(default=False, nullable=False)

    procedure: Mapped["ProcedureResult"] = relationship(back_populates="required_documents")
