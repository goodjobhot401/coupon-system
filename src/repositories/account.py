from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.account import Account


class AccountRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_seeds(self):
        account1 = Account(name="test_user_1")
        account2 = Account(name="test_user_2")
        self.db.add_all([account1, account2])
        await self.db.flush()
        return True

    async def get_account_by_id(self, account_id: int) -> Account | None:
        result = await self.db.execute(
            select(Account)
            .where(Account.id == account_id)
            .with_for_update()
        )
        return result.scalar_one_or_none()

    async def create_account(self, name: str) -> Account:
        account = Account(name=name)
        self.db.add(account)
        return account
