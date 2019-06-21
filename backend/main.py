import logging
from aiohttp import web
from routes import setup_routes
import aiohttp_cors

def init_app():
    app = web.Application()
    cors = aiohttp_cors.setup(app)

    setup_routes(app, cors)
    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    app = init_app()
    web.run_app(app, host='127.0.0.1', port=8081)

main()