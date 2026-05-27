from fastapi import APIRouter

router = APIRouter()


@router.post("/resolve")
def resolve_location() -> dict[str, str]:
    return {"status": "not_implemented"}


@router.post("/parcel-profile")
def create_parcel_profile() -> dict[str, str]:
    return {"status": "not_implemented"}

