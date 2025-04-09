import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from workers.claim_worker import handle_queue_message
from workers.init_group import init_redis_group
from routers.routers import router
from infra.redis import redis_client
from infra.mysql import get_mysql_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start before server initialize
    await init_redis_group(redis_client)

    # start background worker
    mysql = get_mysql_session()
    mysql_client = await mysql.__anext__()
    asyncio.create_task(handle_queue_message(redis_client, mysql_client))

    # server start
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)
