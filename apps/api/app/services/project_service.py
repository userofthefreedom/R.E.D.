from sqlalchemy.orm import Session

from app.db.repositories.project_repository import ProjectRepository
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, session: Session) -> None:
        self.repository = ProjectRepository(session)

    def create_project(self, payload: ProjectCreate) -> Project:
        return self.repository.create(payload)

    def list_projects(self, *, limit: int = 50, offset: int = 0) -> list[Project]:
        return self.repository.list(limit=limit, offset=offset)

    def get_project(self, project_id: str) -> Project | None:
        return self.repository.get(project_id)

    def update_project(self, project_id: str, payload: ProjectUpdate) -> Project | None:
        project = self.repository.get(project_id)
        if project is None:
            return None
        return self.repository.update(project, payload)
