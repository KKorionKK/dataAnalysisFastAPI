from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from api.services.config import get_connection_string
from api.services.models import Base

engine = create_async_engine(get_connection_string(), echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)


async def init_db():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
