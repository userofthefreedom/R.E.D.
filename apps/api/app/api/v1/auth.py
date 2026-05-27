from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
def read_current_user() -> dict[str, str]:
    return {"status": "anonymous"}


@router.post("/login")
def login() -> dict[str, str]:
    return {"status": "not_implemented"}


@router.post("/register")
def register() -> dict[str, str]:
    return {"status": "not_implemented"}


@router.get("/notifications")
def list_notifications() -> list[dict[str, str]]:
    return []

