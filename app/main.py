import asyncio
import os
from contextlib import asynccontextmanager

import asyncpg
import redis.asyncio as redis
from celery import Celery
from fastapi import FastAPI
from loguru import logger

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")

REDIS_URL = CELERY_RESULT_BACKEND

DATABASE_URL = os.environ.get("DATABASE_URL")

celery = Celery(__name__, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name="tasks.check_health")
def healthcheck():
    return "✅ Celery health is ok"


async def connect_redis(app: FastAPI):
    logger.info("🚀 Connecting to Redis...")
    logger.debug(f"{REDIS_URL = }")
    for attempt in range(5):
        try:
            client = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
            await client.ping()
            app.state.redis_client = client
            logger.info("✅ Redis connection successful!")
            return
        except Exception as e:
            logger.error(
                f"❌ Could not connect to Redis (Attempt {attempt + 1}/5): {e}"
            )
            await asyncio.sleep(2**attempt)

    app.state.redis_client = None
    logger.error("❌ Failed to connect to Redis after several retries.")


async def close_redis(app: FastAPI):
    if hasattr(app.state, "redis_client") and app.state.redis_client:
        await app.state.redis_client.close()
        logger.info("🛑 Redis connection closed.")


async def connect_postgres(app: FastAPI):
    logger.info("🚀 Connecting to PostgreSQL...")
    for attempt in range(5):
        try:
            pool = await asyncpg.create_pool(DATABASE_URL)
            version = await pool.fetchval("SELECT version();")
            logger.info(
                f"✅ PostgreSQL connection successful. Version: {version.split(',')[0]}"
            )
            app.state.pg_pool = pool
            return
        except Exception as e:
            logger.error(
                f"❌ Could not connect to PostgreSQL (Attempt {attempt + 1}/5): {e}"
            )
            await asyncio.sleep(2**attempt)

    app.state.pg_pool = None
    logger.error("❌ Failed to connect to PostgreSQL after several retries.")


async def close_postgres(app: FastAPI):
    if hasattr(app.state, "pg_pool") and app.state.pg_pool:
        await app.state.pg_pool.close()
        logger.info("🛑 PostgreSQL connection pool closed.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_redis(app)
    await connect_postgres(app)

    yield

    await close_redis(app)
    await close_postgres(app)


app = FastAPI(title="HomeManager API", version="1.0.0", lifespan=lifespan)


@app.get("/")
def health_check() -> bool:
    healthcheck.delay()
    return True
