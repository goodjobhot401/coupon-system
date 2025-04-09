from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.account import AccountRepository
from repositories.coupon_record import CouponRecordRepository


class AccountService():
    def __init__(self, db: AsyncSession):
        self.db = db
        self.account = AccountRepository(db)
        self.record = CouponRecordRepository(db)

    async def create_seeds(self):
        result = await self.account.create_seeds()
        if result:
            await self.db.commit()
            return True
        return False

    async def get_account_detail(self, account_id):
        raw_account = await self.account.get_account_by_id(account_id)
        account = raw_account.as_dict()

        raw_counpons = await self.record.get_record_by_account_id(account_id)
        coupons = []
        for raw_counpon in raw_counpons:
            coupon = dict()
            used_at = raw_counpon.used_at
            claim_at = raw_counpon.claim_at
            expires_at = raw_counpon.coupon.expires_at

            if used_at:
                status = "used"
            elif expires_at and expires_at < datetime.now():
                status = "expired"
            else:
                status = "unused"

            coupon = {
                "record_id": raw_counpon.id,
                "coupon_id": raw_counpon.coupon_id,
                "status": status,
                "claim_at": claim_at,
                "used_at": used_at,
                "expires_at": expires_at,
            }
            coupons.append(coupon)

        account["coupon_total"] = len(coupons)
        account["coupon_detail"] = coupons
        account.pop("created_at")
        account.pop("updated_at")
        return account

    async def create_account(self, name):
        account = await self.account.create_account(name)
        await self.db.commit()
        await self.db.refresh(account)
        return account
