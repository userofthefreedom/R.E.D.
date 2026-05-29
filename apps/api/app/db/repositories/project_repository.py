from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, payload: ProjectCreate) -> Project:
        project = Project(**payload.model_dump())
        self.session.add(project)
        self.session.flush()
        self.session.refresh(project)
        return project

    def list(self, *, limit: int = 50, offset: int = 0) -> list[Project]:
        statement: Select[tuple[Project]] = (
            select(Project)
            .order_by(Project.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(statement))

    def get(self, project_id: str) -> Project | None:
        return self.session.get(Project, project_id)

    def update(self, project: Project, payload: ProjectUpdate) -> Project:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(project, key, value)
        self.session.flush()
        self.session.refresh(project)
        return project
