from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.coupon import Coupon
from helpers.time import format_datetime_str_to_datetime


class CouponRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_seeds(self):
        raw_data = [
            # (title, type, stock, expires_at)
            ("王品牛排兌換券", "discount", 1000, "2026-01-01T12:30:00"),
            ("路易莎VIP", "discount", 2000, "2025-12-31T23:59:00"),
            ("隨意鳥地方8折券", "discount", 50, "2024-04-08T15:30:00"),
        ]

        seed_data = [Coupon(
            title=data[0],
            type=data[1],
            stock=data[2],
            expires_at=format_datetime_str_to_datetime(data[3])
        ) for data in raw_data]

        self.db.add_all(seed_data)
        await self.db.flush()
        return True

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
