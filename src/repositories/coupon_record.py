from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from models.coupon_record import CouponRecord


class CouponRecordRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_record_by_id(self, record_id: int) -> CouponRecord:
        result = await self.db.execute(
            select(CouponRecord)
            .options(selectinload(CouponRecord.coupon))
            .where(CouponRecord.id == record_id)
            .with_for_update()
        )
        return result.scalar_one_or_none()

    async def get_record_by_account_id(self, account_id: int) -> list | None:
        result = await self.db.execute(
            select(CouponRecord)
            .options(selectinload(CouponRecord.coupon))
            .where(CouponRecord.account_id == account_id)
            .with_for_update()
        )
        return result.scalars().all()

    async def create_record(self, coupon_id: int, account_id: int):
        record = CouponRecord(
            coupon_id=coupon_id,
            account_id=account_id
        )
        self.db.add(record)
        return record

    async def update_used_at(self, record_id: int):
        result = await self.db.execute(
            update(CouponRecord)
            .where(CouponRecord.id == record_id)
            .values(used_at=datetime.now())
        )
        return result
