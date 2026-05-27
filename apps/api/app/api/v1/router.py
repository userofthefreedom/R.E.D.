from fastapi import APIRouter

from app.api.v1 import actions, auth, diagnosis, evidence, locations, projects, reports, support

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(projects.router, prefix="/projects", tags=["projects"])
router.include_router(locations.router, prefix="/locations", tags=["locations"])
router.include_router(actions.router, prefix="/actions", tags=["actions"])
router.include_router(diagnosis.router, prefix="/diagnosis", tags=["diagnosis"])
router.include_router(evidence.router, prefix="/evidence", tags=["evidence"])
router.include_router(reports.router, prefix="/reports", tags=["reports"])
router.include_router(support.router, prefix="/support", tags=["support"])

