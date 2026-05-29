from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.regulation_overlay import RegulationOverlay
from app.schemas.regulation_overlay import RegulationOverlayCreate


class RegulationOverlayRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, project_id: str, payload: RegulationOverlayCreate) -> RegulationOverlay:
        overlay = RegulationOverlay(project_id=project_id, **payload.model_dump())
        self.session.add(overlay)
        self.session.flush()
        self.session.refresh(overlay)
        return overlay

    def list_by_project(self, project_id: str) -> list[RegulationOverlay]:
        statement: Select[tuple[RegulationOverlay]] = (
            select(RegulationOverlay)
            .where(RegulationOverlay.project_id == project_id)
            .order_by(RegulationOverlay.created_at.desc())
        )
        return list(self.session.scalars(statement))

    def get_by_project(self, project_id: str, overlay_id: str) -> RegulationOverlay | None:
        statement: Select[tuple[RegulationOverlay]] = select(RegulationOverlay).where(
            RegulationOverlay.id == overlay_id,
            RegulationOverlay.project_id == project_id,
        )
        return self.session.scalar(statement)
