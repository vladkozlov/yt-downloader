import argparse
import asyncio
import logging
import os
import sys
import datetime
import time
from asyncio.events import get_event_loop

import aiohttp_cors
from aiohttp import web

from backend.db import setup_redis
from backend.routes import setup_routes
from backend.utils import setup_executor

parser = argparse.ArgumentParser(description="YouTube Video Downloader backend")
parser.add_argument('--path')
parser.add_argument('--port')
parser.add_argument('--host')
parser.add_argument('--logs')
parser.add_argument('--redisocket')

async def init_app(config):
    app = web.Application()
    cors = aiohttp_cors.setup(app)
    (executor, close_executor) = await setup_executor(app)
    
    app.on_cleanup.append(close_executor)
    app['executor'] = executor

    setup_routes(app, cors)

    (redis_pool, close_redis) = await setup_redis(socket=config['redisocket'], host='127.0.0.1', port=6379)
    app.on_cleanup.append(close_redis)
    app['redis_pool'] = redis_pool

    return app


def main(argv):
    args = parser.parse_args()
    config = {
        "path": args.path or None,
        "port": args.port or 8089,
        "host": args.host or '127.0.0.1',
        "logs": args.logs or 'logs/ytdloader_backend.log',
        "redisocket": args.redisocket or None
    }

    log_file = config['logs']

    os.makedirs(os.path.dirname(log_file),exist_ok=True)
    
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG)

    logging.info('{0} - APP_STARTED'.format(datetime.datetime.fromtimestamp(time.time()).isoformat()))
    logging.info('Config {0}'.format(config))

    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app(config))


    
    if config['path']:
        web.run_app(app, path=config['path'], port=int(config['port']))
    else:
        web.run_app(app, host=config['host'], port=int(config['port']))

if __name__ == '__main__':
    main(sys.argv[1:])
