from fastapi import Depends
from fastapi import APIRouter
from services.coupon import CouponService
from infra.mysql import get_mysql_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/all")
async def get_coupons(db: AsyncSession = Depends(get_mysql_session)):
    service = CouponService(db=db)
    return await service.get_coupons()
