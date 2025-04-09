from fastapi import Depends
from fastapi import APIRouter
from infra.mysql import get_mysql_session
from services.account import AccountService
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/{account_id}")
async def get_account_detail(
        account_id,
        db: AsyncSession = Depends(get_mysql_session)):
    service = AccountService(db=db)
    return await service.get_account_detail(account_id)
