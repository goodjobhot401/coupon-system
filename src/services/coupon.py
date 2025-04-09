from sqlalchemy.ext.asyncio import AsyncSession
from repositories.coupon import CouponRepository


class CouponService():
    def __init__(self, db: AsyncSession):
        self.db = db
        self.coupon = CouponRepository(db)

    async def get_coupons(self):
        raw_coupons = await self.coupon.get_coupons()
        coupons = list()
        for raw_coupon in raw_coupons:
            coupon = raw_coupon.as_dict()
            coupon.pop("created_at")
            coupon.pop("updated_at")
            coupons.append(coupon)
        return coupons
