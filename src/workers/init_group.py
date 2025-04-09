async def init_redis_group(redis):
    stream_name = "coupon_claim_queue"
    group_name = "coupon_group"

    await redis.delete(stream_name)

    # 'redis.scan_iter' use 'async for'
    keys = [key async for key in redis.scan_iter("coupon:*")]
    if keys:
        await redis.delete(*keys)

    await redis.xgroup_create(
        name=stream_name,
        groupname=group_name,
        id="0",
        mkstream=True
    )
