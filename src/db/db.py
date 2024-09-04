from core.config import app_settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from os import getenv
from dotenv import load_dotenv
load_dotenv()


#url = 'postgresql+asyncpg://postgres:postgres@localhost:5432/collection'
engine = create_async_engine(getenv('DATABASE_DSN'), echo=True, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session 