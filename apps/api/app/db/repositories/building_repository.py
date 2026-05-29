from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.building import Building
from app.schemas.building import BuildingCreate


class BuildingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, project_id: str, payload: BuildingCreate) -> Building:
        building = Building(project_id=project_id, **payload.model_dump())
        self.session.add(building)
        self.session.flush()
        self.session.refresh(building)
        return building

    def list_by_project(self, project_id: str) -> list[Building]:
        statement: Select[tuple[Building]] = (
            select(Building)
            .where(Building.project_id == project_id)
            .order_by(Building.created_at.desc())
        )
        return list(self.session.scalars(statement))

    def get_by_project(self, project_id: str, building_id: str) -> Building | None:
        statement: Select[tuple[Building]] = select(Building).where(
            Building.id == building_id,
            Building.project_id == project_id,
        )
        return self.session.scalar(statement)
