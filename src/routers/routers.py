from fastapi import APIRouter
from routers.endpoints.account_controller import router as account_router
from routers.endpoints.coupon_controller import router as coupon_router

router = APIRouter()

router.include_router(account_router, prefix="/account", tags=["Account"])
router.include_router(coupon_router, prefix="/coupon", tags=["Coupon"])
