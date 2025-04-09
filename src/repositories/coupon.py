from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.coupon import Coupon


class CouponRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_coupons(self) -> list:
        result = await self.db.execute(
            select(Coupon)
        )
        return result.scalars().all()
