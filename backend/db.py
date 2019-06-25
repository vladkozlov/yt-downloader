import aioredis
from aiohttp import web
import asyncio

async def setup_redis(host, port, socket=None):
    loop = asyncio.get_event_loop()
    
    pool = None
    if socket:
        pool = await aioredis.create_redis_pool(socket, loop=loop)
    else:
        pool = await aioredis.create_redis_pool(
            (host, port),
            loop=loop
        )

    async def close_redis():
        pool.close()
        await pool.wait_closed()

    return (pool, close_redis)