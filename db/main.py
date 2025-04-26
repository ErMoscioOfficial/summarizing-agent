from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import config

from db.models import Users

engine = create_async_engine(
    url = config.DATABASE_URL,
    echo = True
)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind = engine,
        class_ = AsyncSession,
        expire_on_commit = False
    )

    async with Session() as session:
        yield session
