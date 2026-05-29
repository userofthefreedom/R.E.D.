from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter()


def get_project_service(session: Session = Depends(get_session)) -> ProjectService:
    return ProjectService(session)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    session: Session = Depends(get_session),
) -> ProjectRead:
    service = ProjectService(session)
    project = service.create_project(payload)
    session.commit()
    return project


@router.get("", response_model=list[ProjectRead])
def list_projects(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectRead]:
    return service.list_projects(limit=limit, offset=offset)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service),
) -> ProjectRead:
    project = service.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: str,
    payload: ProjectUpdate,
    session: Session = Depends(get_session),
) -> ProjectRead:
    service = ProjectService(session)
    project = service.update_project(project_id, payload)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    session.commit()
    return project


@router.get("/{project_id}/reports")
def list_project_reports(project_id: str) -> list[dict[str, str]]:
    return []


@router.get("/{project_id}/history")
def list_project_history(project_id: str) -> list[dict[str, str]]:
    return []


@router.get("/{project_id}/snapshots/compare")
def compare_project_snapshots(project_id: str) -> dict[str, str]:
    return {"project_id": project_id, "status": "not_implemented"}
