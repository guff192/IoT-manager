from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

async_engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URL))


async def db_ready():
    async with async_engine.connect() as connection:
        await connection.execute(text("SELECT version()"))
