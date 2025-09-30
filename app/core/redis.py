import asyncio

import redis.asyncio as redis
from fastapi import FastAPI
from loguru import logger

from app.core.config import settings


async def connect_redis(app: FastAPI):
    logger.info("🚀 Connecting to Redis...")
    logger.debug(f"{settings.REDIS_URL = }")
    for attempt in range(5):
        try:
            client = redis.from_url(
                settings.REDIS_URL, encoding="utf-8", decode_responses=True
            )
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
