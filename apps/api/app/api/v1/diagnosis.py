from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.repositories.action_repository import ActionRepository
from app.db.repositories.diagnosis_repository import DiagnosisRepository
from app.db.repositories.project_repository import ProjectRepository
from app.db.session import get_session
from app.schemas.diagnosis import DiagnosisRunCreate, DiagnosisRunRead, DiagnosisStatusRead
from app.services.rule_engine_service import RuleEngineService

router = APIRouter()


def ensure_project_and_action(session: Session, payload: DiagnosisRunCreate) -> None:
    if ProjectRepository(session).get(payload.project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if payload.action_id and ActionRepository(session).get_by_project(payload.project_id, payload.action_id) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Action does not belong to project",
        )


def get_existing_run(session: Session, run_id: str):
    run = DiagnosisRepository(session).get_run(run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diagnosis run not found")
    return run


@router.post("/runs", response_model=DiagnosisRunRead, status_code=status.HTTP_201_CREATED)
def create_diagnosis_run(
    payload: DiagnosisRunCreate,
    session: Session = Depends(get_session),
) -> DiagnosisRunRead:
    ensure_project_and_action(session, payload)
    run = DiagnosisRepository(session).create_run(payload)
    session.commit()
    return run


@router.get("/runs/{run_id}", response_model=DiagnosisRunRead)
def get_diagnosis_run(
    run_id: str,
    session: Session = Depends(get_session),
) -> DiagnosisRunRead:
    return get_existing_run(session, run_id)


@router.get("/runs/{run_id}/status", response_model=DiagnosisStatusRead)
def get_diagnosis_status(
    run_id: str,
    session: Session = Depends(get_session),
) -> DiagnosisStatusRead:
    run = get_existing_run(session, run_id)
    return DiagnosisStatusRead(
        run_id=run.id,
        status=run.status,
        message="Prototype diagnosis run completed with mock rule/RAG outputs.",
    )


@router.get("/runs/{run_id}/result")
def get_diagnosis_result(
    run_id: str,
    session: Session = Depends(get_session),
) -> dict:
    run = get_existing_run(session, run_id)
    return RuleEngineService(session).evaluate_run(run)


@router.get("/runs/{run_id}/evidence")
def get_diagnosis_evidence(run_id: str) -> list[dict[str, str]]:
    return []


@router.get("/runs/{run_id}/trace")
def get_diagnosis_trace(
    run_id: str,
    session: Session = Depends(get_session),
) -> list[dict]:
    run = get_existing_run(session, run_id)
    return RuleEngineService(session).evaluate_run(run)["rule_traces"]


@router.get("/runs/{run_id}/alternatives")
def get_alternative_scenarios(run_id: str) -> list[dict[str, str]]:
    return []

