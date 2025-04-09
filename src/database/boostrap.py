import asyncio
from infra.session import engine
from models.base import Base
from models.account import Account
from models.coupon import Coupon


async def bootstrap():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(bootstrap())
