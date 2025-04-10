from .session import AsyncSessionLocal


async def get_mysql_session():
    async with AsyncSessionLocal() as session:
        yield session
