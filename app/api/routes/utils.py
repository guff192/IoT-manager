from fastapi import APIRouter

from app.tasks.utils import healthcheck


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check/")
def health_check() -> bool:
    healthcheck.delay()
    return True
