from datetime import UTC, datetime

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.diagnosis_run import DiagnosisRun
from app.schemas.diagnosis import DiagnosisRunCreate


class DiagnosisRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_run(self, payload: DiagnosisRunCreate) -> DiagnosisRun:
        now = datetime.now(UTC)
        run = DiagnosisRun(
            project_id=payload.project_id,
            action_id=payload.action_id,
            status="completed",
            rule_set_version=payload.rule_set_version,
            rag_index_version=payload.rag_index_version,
            data_base_date=payload.data_base_date,
            law_base_date=payload.law_base_date,
            started_at=now,
            completed_at=now,
        )
        self.session.add(run)
        self.session.flush()
        self.session.refresh(run)
        return run

    def get_run(self, run_id: str) -> DiagnosisRun | None:
        return self.session.get(DiagnosisRun, run_id)

    def list_by_project(self, project_id: str) -> list[DiagnosisRun]:
        statement: Select[tuple[DiagnosisRun]] = (
            select(DiagnosisRun)
            .where(DiagnosisRun.project_id == project_id)
            .order_by(DiagnosisRun.created_at.desc())
        )
        return list(self.session.scalars(statement))
