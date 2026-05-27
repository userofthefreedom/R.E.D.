from fastapi import APIRouter

router = APIRouter()


@router.get("/{evidence_id}")
def get_evidence(evidence_id: str) -> dict[str, str]:
    return {"evidence_id": evidence_id}

