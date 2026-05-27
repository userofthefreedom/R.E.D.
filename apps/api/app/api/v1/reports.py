from fastapi import APIRouter

router = APIRouter()


@router.post("")
def create_report() -> dict[str, str]:
    return {"status": "not_implemented"}


@router.get("/{report_id}")
def get_report(report_id: str) -> dict[str, str]:
    return {"report_id": report_id}


@router.get("/{report_id}/download")
def download_report(report_id: str) -> dict[str, str]:
    return {"report_id": report_id, "status": "not_implemented"}

