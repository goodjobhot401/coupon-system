import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DB_USER = os.getenv("MYSQL_USER", "")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_HOST = os.getenv("MYSQL_HOST", "")
DB_PORT = os.getenv("MYSQL_PORT", 0)
DB_NAME = os.getenv("MYSQL_DATABASE", "")
DATABASE_URL = f"mysql+asyncmy://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
