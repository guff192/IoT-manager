import asyncio
from fastapi import FastAPI
from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings

async_engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URL))


async def connect_async_db(app: FastAPI):
    logger.info("🚀 Connecting to Redis...")
    logger.debug(f"{settings.SQLALCHEMY_DATABASE_URL = }")
    for attempt in range(5):
        try:
            async_engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URL))

            app.state.db_async_engine = async_engine
            logger.info("✅ Postgres connection successful!")
            return
        except Exception as e:
            logger.error(
                f"❌ Could not connect to Postgres (Attempt {attempt + 1}/5): {e}"
            )
            await asyncio.sleep(2**attempt)

    app.state.db_async_engine = None
    logger.error("❌ Failed to connect to Postgres after several retries.")


async def close_async_db(app: FastAPI):
    if hasattr(app.state, "db_async_engine") and app.state.db_async_engine:
        async_engine: AsyncEngine = app.state.db_async_engine
        await async_engine.dispose(close=True)
        logger.info("🛑 Postgres connection closed.")
        return

    logger.error("❌ Postgres connection not found.")



async def db_ready(app: FastAPI):
    if hasattr(app.state, "db_async_engine") and app.state.db_async_engine:
        async_engine: AsyncEngine = app.state.db_async_engine
        async with async_engine.connect() as connection:
            result = await connection.execute(text("SELECT version()"))
            logger.info(f"Postgres version: {result.scalar()}")
        return

    logger.error("❌ Postgres connection not found.") 
