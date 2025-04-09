from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = f"mysql+asyncmy://coupon-system-user:coupon-system-password@mysql:3306/coupon-system"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
