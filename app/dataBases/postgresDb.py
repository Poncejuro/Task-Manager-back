from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.sql import text
from app.dataBases.base import Base 
from app.models.task import Task
from app.core.config import settings
from typing import AsyncGenerator

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL, echo=True)
metadata = MetaData()

SessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def create_schema():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS schedule;"))
        print(f"Schema 'schedule' created successfully.")

async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(f"Tables created successfully.")
        
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db_session:
        yield db_session
