from fastapi import Depends
from fastapi import APIRouter
from services.coupon import CouponService
from services.record import CouponRecordService
from infra.mysql import get_mysql_session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.record import ClaimCouponRequest

router = APIRouter()


@router.get("/all")
async def get_coupons(db: AsyncSession = Depends(get_mysql_session)):
    service = CouponService(db=db)
    return await service.get_coupons()


@router.post("/use/{record_id}")
async def use_coupon(
        record_id,
        db: AsyncSession = Depends(get_mysql_session)):
    service = CouponRecordService(db=db)
    return await service.use_coupon(record_id)


@router.post("/{coupon_id}")
async def claim_coupon(
        coupon_id,
        req: ClaimCouponRequest,
        db: AsyncSession = Depends(get_mysql_session)):
    service = CouponRecordService(db=db)
    return await service.claim_coupon(coupon_id, account_id=req.account_id)
