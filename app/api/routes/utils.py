from fastapi import APIRouter

from app.tasks.main import healthcheck_task


router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check/")
def health_check() -> bool:
    healthcheck_task.delay()  # type: ignore
    return True
