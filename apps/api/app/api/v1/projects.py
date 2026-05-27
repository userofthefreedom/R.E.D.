from fastapi import APIRouter

router = APIRouter()


@router.post("")
def create_project() -> dict[str, str]:
    return {"status": "not_implemented"}


@router.get("")
def list_projects() -> list[dict[str, str]]:
    return []


@router.get("/{project_id}")
def get_project(project_id: str) -> dict[str, str]:
    return {"project_id": project_id}

