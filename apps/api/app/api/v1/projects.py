from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.repositories.action_repository import ActionRepository
from app.db.repositories.building_repository import BuildingRepository
from app.db.repositories.parcel_repository import ParcelRepository
from app.db.repositories.regulation_overlay_repository import RegulationOverlayRepository
from app.db.session import get_session
from app.schemas.action import ActionCreate, ActionRead
from app.schemas.building import BuildingCreate, BuildingRead
from app.schemas.parcel import ParcelCreate, ParcelRead
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.schemas.regulation_overlay import RegulationOverlayCreate, RegulationOverlayRead
from app.services.project_service import ProjectService

router = APIRouter()


def get_project_service(session: Session = Depends(get_session)) -> ProjectService:
    return ProjectService(session)


def ensure_project_exists(service: ProjectService, project_id: str) -> None:
    if service.get_project(project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


def ensure_parcel_belongs_to_project(session: Session, project_id: str, parcel_id: str | None) -> None:
    if parcel_id is None:
        return
    if ParcelRepository(session).get_by_project(project_id, parcel_id) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parcel does not belong to project",
        )


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


@router.post("/{project_id}/parcels", response_model=ParcelRead, status_code=status.HTTP_201_CREATED)
def create_project_parcel(
    project_id: str,
    payload: ParcelCreate,
    session: Session = Depends(get_session),
) -> ParcelRead:
    service = ProjectService(session)
    ensure_project_exists(service, project_id)
    parcel = ParcelRepository(session).create(project_id, payload)
    session.commit()
    return parcel


@router.get("/{project_id}/parcels", response_model=list[ParcelRead])
def list_project_parcels(
    project_id: str,
    session: Session = Depends(get_session),
) -> list[ParcelRead]:
    service = ProjectService(session)
    ensure_project_exists(service, project_id)
    return ParcelRepository(session).list_by_project(project_id)


@router.post("/{project_id}/buildings", response_model=BuildingRead, status_code=status.HTTP_201_CREATED)
def create_project_building(
    project_id: str,
    payload: BuildingCreate,
    session: Session = Depends(get_session),
) -> BuildingRead:
    service = ProjectService(session)
    ensure_project_exists(service, project_id)
    ensure_parcel_belongs_to_project(session, project_id, payload.parcel_id)
    building = BuildingRepository(session).create(project_id, payload)
    session.commit()
    return building


@router.get("/{project_id}/buildings", response_model=list[BuildingRead])
def list_project_buildings(
    project_id: str,
    session: Session = Depends(get_session),
) -> list[BuildingRead]:
    service = ProjectService(session)
    ensure_project_exists(service, project_id)
    return BuildingRepository(session).list_by_project(project_id)


@router.post("/{project_id}/actions", response_model=ActionRead, status_code=status.HTTP_201_CREATED)
def create_project_action(
    project_id: str,
    payload: ActionCreate,
    session: Session = Depends(get_session),
) -> ActionRead:
    service = ProjectService(session)
    ensure_project_exists(service, project_id)
    action = ActionRepository(session).create(project_id, payload)
    session.commit()
    return action


@router.get("/{project_id}/actions", response_model=list[ActionRead])
def list_project_actions(
    project_id: str,
    session: Session = Depends(get_session),
) -> list[ActionRead]:
    service = ProjectService(session)
    ensure_project_exists(service, project_id)
    return ActionRepository(session).list_by_project(project_id)


@router.post("/{project_id}/regulation-overlays", response_model=RegulationOverlayRead, status_code=status.HTTP_201_CREATED)
def create_project_regulation_overlay(
    project_id: str,
    payload: RegulationOverlayCreate,
    session: Session = Depends(get_session),
) -> RegulationOverlayRead:
    service = ProjectService(session)
    ensure_project_exists(service, project_id)
    ensure_parcel_belongs_to_project(session, project_id, payload.parcel_id)
    overlay = RegulationOverlayRepository(session).create(project_id, payload)
    session.commit()
    return overlay


@router.get("/{project_id}/regulation-overlays", response_model=list[RegulationOverlayRead])
def list_project_regulation_overlays(
    project_id: str,
    session: Session = Depends(get_session),
) -> list[RegulationOverlayRead]:
    service = ProjectService(session)
    ensure_project_exists(service, project_id)
    return RegulationOverlayRepository(session).list_by_project(project_id)
