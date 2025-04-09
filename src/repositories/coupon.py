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

    async def get_coupon_by_id(self, coupon_id) -> Coupon | None:
        result = await self.db.execute(
            select(Coupon)
            .where(Coupon.id == coupon_id)
            .with_for_update()
        )
        return result.scalar_one_or_none()

    async def decrease_stock(self, coupon_id) -> Coupon | None:
        result = await self.db.execute(
            select(Coupon)
            .where(Coupon.id == coupon_id)
            .with_for_update()
        )
        coupon = result.scalar_one_or_none()

        if not coupon:
            return None
        elif coupon.stock <= 0:
            return None

        coupon.stock -= 1
        self.db.add(coupon)
        return coupon
