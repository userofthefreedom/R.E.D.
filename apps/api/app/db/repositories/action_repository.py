from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.action import Action
from app.schemas.action import ActionCreate


class ActionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, project_id: str, payload: ActionCreate) -> Action:
        action = Action(project_id=project_id, **payload.model_dump())
        self.session.add(action)
        self.session.flush()
        self.session.refresh(action)
        return action

    def list_by_project(self, project_id: str) -> list[Action]:
        statement: Select[tuple[Action]] = (
            select(Action)
            .where(Action.project_id == project_id)
            .order_by(Action.created_at.desc())
        )
        return list(self.session.scalars(statement))

    def get_by_project(self, project_id: str, action_id: str) -> Action | None:
        statement: Select[tuple[Action]] = select(Action).where(
            Action.id == action_id,
            Action.project_id == project_id,
        )
        return self.session.scalar(statement)
