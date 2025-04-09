from pydantic import BaseModel


class ClaimCouponRequest(BaseModel):
    account_id: int
