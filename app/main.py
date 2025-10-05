import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings
from app.core.db import close_async_db, connect_async_db, db_ready
from app.core.redis import close_redis, connect_redis

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")

REDIS_URL = CELERY_RESULT_BACKEND

DATABASE_URL = os.environ.get("DATABASE_URL")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_redis(app)
    await connect_async_db(app)
    await db_ready(app)

    yield

    await close_async_db(app)
    await close_redis(app)


app = FastAPI(title="HomeManager API", version="1.0.0", lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)
