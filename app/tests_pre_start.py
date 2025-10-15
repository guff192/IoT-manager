import asyncio

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel import select

from app.core.db import async_engine


async def init(db_engine: AsyncEngine) -> None:
    for attempt in range(5):
        try:
            async with AsyncSession(db_engine) as session:
                await session.execute(select(1))
            return
        except Exception as e:
            logger.error(
                f"❌ Could not connect to Postgres (Attempt {attempt + 1}/5): {e}"
            )
            await asyncio.sleep(2**attempt)


async def main() -> None:
    logger.info("Initializing database for tests")
    await init(db_engine=async_engine)
    logger.info("✅ Database initialized for tests")


if __name__ == "__main__":
    asyncio.run(main())
