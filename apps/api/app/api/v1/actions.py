from fastapi import APIRouter

router = APIRouter()


@router.post("/normalize")
def normalize_action() -> dict[str, str]:
    return {"status": "not_implemented"}

