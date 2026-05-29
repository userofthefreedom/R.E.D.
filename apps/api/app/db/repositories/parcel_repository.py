from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.parcel import Parcel
from app.schemas.parcel import ParcelCreate


class ParcelRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, project_id: str, payload: ParcelCreate) -> Parcel:
        parcel = Parcel(project_id=project_id, **payload.model_dump())
        self.session.add(parcel)
        self.session.flush()
        self.session.refresh(parcel)
        return parcel

    def list_by_project(self, project_id: str) -> list[Parcel]:
        statement: Select[tuple[Parcel]] = (
            select(Parcel)
            .where(Parcel.project_id == project_id)
            .order_by(Parcel.created_at.desc())
        )
        return list(self.session.scalars(statement))

    def get_by_project(self, project_id: str, parcel_id: str) -> Parcel | None:
        statement: Select[tuple[Parcel]] = select(Parcel).where(
            Parcel.id == parcel_id,
            Parcel.project_id == project_id,
        )
        return self.session.scalar(statement)
