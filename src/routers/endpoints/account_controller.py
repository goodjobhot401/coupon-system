from fastapi import Depends
from fastapi import APIRouter
from infra.mysql import get_mysql_session
from services.account import AccountService
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.account import CreateAccountRequest


router = APIRouter()


@router.get("/{account_id}")
async def get_account_detail(
        account_id,
        db: AsyncSession = Depends(get_mysql_session)):
    service = AccountService(db=db)
    return await service.get_account_detail(account_id)


@router.post("/create")
async def create_account(
        req: CreateAccountRequest,
        db: AsyncSession = Depends(get_mysql_session)):
    service = AccountService(db=db)
    return await service.create_account(name=req.name)
