import json
import asyncio
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.coupon import CouponRepository
from repositories.coupon_record import CouponRecordRepository


async def handle_queue_message(
        redis: Redis,
        db: AsyncSession):
    while True:
        try:
            response = await redis.xreadgroup(
                groupname="coupon_group",
                consumername="worker-1",
                streams={"coupon_claim_queue": ">"},
                count=10,
                block=5000
            )

            if not response:
                print("No message. Worker sleeping...")
                await asyncio.sleep(1)
                continue

            """
            Redis Stream message (example)
            response = [(
                    'coupon_claim_queue',  # stream_name
                    [
                        (
                            '1744019344208-0',  # message_id
                            {
                                'coupon_id': '"1"',
                                'account_id': '2',
                                'claimed_at': '"2025-04-07T17:49:04.208411"'
                            }
                        ),
                        (
                            '1744019344208-1',
                            {
                                'coupon_id': '"1"',
                                'account_id': '3',
                                'claimed_at': '"2025-04-07T17:49:04.208512"'
                            }
                        )
                    ]
                )]
            """
            for stream_name, messages in response:
                for message_id, message_data in messages:
                    try:
                        data = {
                            key: json.loads(value) for key, value in message_data.items()
                        }

                        coupon_id = int(data["coupon_id"])
                        account_id = int(data["account_id"])

                        coupon = CouponRepository(db)
                        record = CouponRecordRepository(db)

                        decrease_stock = await coupon.decrease_stock(coupon_id)
                        new_record = await record.create_record(
                            coupon_id=coupon_id,
                            account_id=account_id
                        )

                        await db.commit()
                        await db.refresh(decrease_stock)
                        await db.refresh(new_record)
                        print(f"message_id: {message_id} complete")
                        await redis.xack("coupon_claim_queue", "coupon_group", message_id)

                    except Exception as e:
                        print(f"message_id: {message_id}, error: {e}")

        except Exception as e:
            print(f"redis worker failed: {e}")
