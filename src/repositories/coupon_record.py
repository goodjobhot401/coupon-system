from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from models.coupon_record import CouponRecord
from helpers.time import format_datetime_str_to_datetime


class CouponRecordRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_seeds(self):
        raw_data = [
            # (coupon_id, account_id, claim_at)
            (1, 1, "2025-04-07T23:59:00"),
            (2, 1, "2025-04-07T23:59:00"),
            (3, 1, "2023-04-07T23:59:00"),
            (1, 2, "2025-04-07T23:59:00"),
            (2, 2, "2025-04-07T23:59:00"),
            (3, 2, "2023-04-07T23:59:00"),
        ]

        seed_data = [CouponRecord(
            coupon_id=data[0],
            account_id=data[1],
            claim_at=format_datetime_str_to_datetime(data[2])
        ) for data in raw_data]

        self.db.add_all(seed_data)
        await self.db.flush()
        return True

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
