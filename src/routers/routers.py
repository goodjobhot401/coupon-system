from fastapi import APIRouter
from routers.endpoints.account_controller import router as account_router

router = APIRouter()

router.include_router(account_router, prefix="/account", tags=["Account"])
