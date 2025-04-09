import json
from datetime import datetime
from redis.asyncio import Redis
from helpers.time import format_datetime_str_to_datetime
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.coupon import CouponRepository
from repositories.coupon_record import CouponRecordRepository


class CouponRecordService():
    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.redis = redis
        self.coupon = CouponRepository(db)
        self.record = CouponRecordRepository(db)
        self.response = {
            "success": False,
            "code": "",
            "message": ""
        }

    # debug
    async def update_cache(self, coupon_id):
        key = f"coupon:{coupon_id}"
        raw_coupon = await self.coupon.get_coupon_by_id(coupon_id)
        if not raw_coupon:
            return None

        coupon_data = {
            "stock": str(raw_coupon.stock),
            "expires_at": raw_coupon.expires_at.isoformat()
        }
        await self.redis.hset(key, mapping=coupon_data)
        await self.redis.set(f"{key}:stock", raw_coupon.stock)
        return raw_coupon

    async def get_coupon_cache(self, coupon_id):
        key = f"coupon:{coupon_id}"
        coupon_cache = await self.redis.hgetall(key)

        if not coupon_cache:
            raw_coupon = await self.coupon.get_coupon_by_id(coupon_id)
            if not raw_coupon:
                return None

            coupon_data = {
                "stock": str(raw_coupon.stock),
                "expires_at": raw_coupon.expires_at.isoformat()
            }
            await self.redis.hset(key, mapping=coupon_data)
            await self.redis.set(f"{key}:stock", raw_coupon.stock)
            return coupon_data

        return coupon_cache

    async def claim_coupon(self, coupon_id, account_id):
        key = f"coupon:{coupon_id}"
        coupon_cache = await self.get_coupon_cache(coupon_id)

        if not coupon_cache:
            self.response.update({
                "success": False,
                "code": "COUPON_NOT_FOUND",
                "message": "Coupon not found"
            })
            return self.response

        expires_at = coupon_cache.get("expires_at")
        stock = coupon_cache.get("stock")

        if not expires_at or format_datetime_str_to_datetime(expires_at) < datetime.now():
            self.response.update({
                "success": False,
                "code": "COUPON_NOT_FOUND",
                "message": "Coupon expired"
            })
            return self.response

        stock = await self.redis.decr(f"{key}:stock")
        if int(stock) < 0:
            await self.redis.incr(f"{key}:stock")
            self.response.update({
                "code": "OUT_OF_STOCK",
                "message": "Coupon out of stock"
            })
            return self.response

        message = {
            "coupon_id": coupon_id,
            "account_id": account_id,
            "claimed_at": datetime.now().isoformat()
        }

        await self.redis.xadd(
            "coupon_claim_queue",
            {key: json.dumps(value) for key, value in message.items()}
        )

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
