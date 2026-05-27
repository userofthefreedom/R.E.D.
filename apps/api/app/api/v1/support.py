from fastapi import APIRouter

router = APIRouter()


@router.get("/failure-reasons")
def list_failure_reasons() -> list[dict[str, str]]:
    return []


@router.get("/pre-consultation-guides")
def list_pre_consultation_guides() -> list[dict[str, str]]:
    return []
