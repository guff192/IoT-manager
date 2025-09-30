from celery import Celery

from app.core.config import settings
from app.tasks.utils import healthcheck

celery = Celery(
    __name__, broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)

celery.task(healthcheck, name="tasks.check_health")

