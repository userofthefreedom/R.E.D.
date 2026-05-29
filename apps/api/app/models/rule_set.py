from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class RuleSet(IdMixin, TimestampMixin, Base):
    __tablename__ = "rule_sets"

    version: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    effective_date: Mapped[date | None] = mapped_column(Date)
    description: Mapped[str | None] = mapped_column(Text)

    rules: Mapped[list["Rule"]] = relationship(back_populates="rule_set", cascade="all, delete-orphan")
