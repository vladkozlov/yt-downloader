import sys
import argparse
import logging
from aiohttp import web
from backend.routes import setup_routes
import aiohttp_cors

parser = argparse.ArgumentParser(description="YouTube Video Downloader backend")
parser.add_argument('--path')
parser.add_argument('--port')
parser.add_argument('--host')

def init_app():
    app = web.Application()
    cors = aiohttp_cors.setup(app)

    setup_routes(app, cors)
    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)
    
    app = init_app()
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