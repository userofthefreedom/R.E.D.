from typing import Any

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class Rule(IdMixin, TimestampMixin, Base):
    __tablename__ = "rules"

    rule_set_id: Mapped[str] = mapped_column(ForeignKey("rule_sets.id"), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str | None] = mapped_column(String(80))
    input_fields: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    condition_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    result_template: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    description: Mapped[str | None] = mapped_column(Text)

    rule_set: Mapped["RuleSet"] = relationship(back_populates="rules")
