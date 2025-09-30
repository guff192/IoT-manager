import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db import db_ready
from app.core.redis import close_redis, connect_redis

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")

REDIS_URL = CELERY_RESULT_BACKEND

DATABASE_URL = os.environ.get("DATABASE_URL")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_redis(app)
    await db_ready()

    yield

    await close_redis(app)


app = FastAPI(title="HomeManager API", version="1.0.0", lifespan=lifespan)
