from fastapi import APIRouter

router = APIRouter()


@router.post("/runs")
def create_diagnosis_run() -> dict[str, str]:
    return {"status": "not_implemented"}


@router.get("/runs/{run_id}")
def get_diagnosis_run(run_id: str) -> dict[str, str]:
    return {"run_id": run_id}


@router.get("/runs/{run_id}/status")
def get_diagnosis_status(run_id: str) -> dict[str, str]:
    return {"run_id": run_id, "status": "pending"}


@router.get("/runs/{run_id}/result")
def get_diagnosis_result(run_id: str) -> dict[str, str]:
    return {"run_id": run_id}


@router.get("/runs/{run_id}/evidence")
def get_diagnosis_evidence(run_id: str) -> list[dict[str, str]]:
    return []


@router.get("/runs/{run_id}/trace")
def get_diagnosis_trace(run_id: str) -> list[dict[str, str]]:
    return []

