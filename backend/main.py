import argparse
import asyncio
import logging
import sys
from asyncio.events import get_event_loop

import aiohttp_cors
from aiohttp import web

from backend.routes import setup_routes
from backend.utils import setup_executor

parser = argparse.ArgumentParser(description="YouTube Video Downloader backend")
parser.add_argument('--path')
parser.add_argument('--port')
parser.add_argument('--host')

async def init_app():
    app = web.Application()
    cors = aiohttp_cors.setup(app)
    await setup_executor(app)
    setup_routes(app, cors)
    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)
    
    loop = asyncio.get_event_loop()

    app = loop.run_until_complete(init_app())

    args = parser.parse_args()
    logging.info("Program args {0}".format(args))
    config = {
        "path": args.path or None,
        "port": args.port or 8089,
        "host": args.host or '127.0.0.1'
    }
    
    logging.info('Config {0}'.format(config))
    if config['path']:
        web.run_app(app, path=config['path'], port=int(config['port']))
    else:
        web.run_app(app, host=config['host'], port=int(config['port']))

if __name__ == '__main__':
    main(sys.argv[1:])
