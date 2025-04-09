from datetime import datetime
from models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, TIMESTAMP, func


class CouponRecord(Base):
    __tablename__ = "coupon_record"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    coupon_id: Mapped[int] = mapped_column(Integer, ForeignKey("coupon.id"))
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("account.id"))
    claim_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now())
    used_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    account = relationship("Account")
    coupon = relationship("Coupon")
