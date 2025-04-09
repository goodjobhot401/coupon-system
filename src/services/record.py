from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.coupon import CouponRepository
from repositories.coupon_record import CouponRecordRepository


class CouponRecordService():
    def __init__(self, db: AsyncSession):
        self.db = db
        self.coupon = CouponRepository(db)
        self.record = CouponRecordRepository(db)
        self.response = {
            "success": False,
            "code": "",
            "message": ""
        }

    async def claim_coupon(self, coupon_id, account_id):
        raw_coupon = await self.record.get_record_by_id(coupon_id)
        if not raw_coupon:
            self.response.update({
                "code": "COUPON_NOT_FOUND",
                "message": "Coupon not found"
            })
            return self.response

        if raw_coupon.expires_at < datetime.now():
            self.response.update({
                "code": "COUPON_EXPIRED",
                "message": "Coupon expired"
            })
            return self.response

        if raw_coupon.stock == 0:
            self.response.update({
                "code": "OUT_OF_STOCK",
                "message": "Coupon out of stock"
            })
            return self.response

        decrease_stock = await self.coupon.decrease_stock(coupon_id)
        new_record = await self.record.create_record(
            coupon_id=coupon_id,
            account_id=account_id
        )

        await self.db.commit()
        await self.db.refresh(decrease_stock)
        await self.db.refresh(new_record)

        self.response.update({
            "success": True,
            "code": "CLAIM_SUCCESS",
            "message": "Coupon claimed successfully"
        })
        return self.response

    async def use_coupon(self, record_id):
        raw_record = await self.record.get_record_by_id(record_id)
        if not raw_record:
            self.response.update({
                "success": False,
                "code": "USE_FAILED",
                "message": "No record found"
            })
            return self.response

        if raw_record.coupon.expires_at < datetime.now():
            self.response.update({
                "success": False,
                "code": "USE_FAILED",
                "message": "Coupon expired"
            })
            return self.response

        await self.record.update_used_at(record_id)
        await self.db.commit()

        self.response.update({
            "success": True,
            "code": "USE_SUCCESS",
            "message": "Coupon used successfully"
        })
        return self.response
