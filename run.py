import asyncio
from aiohttp import web
from utils import init_workers
from views import ProgressionHandler
from routes import init_routes


async def init_app() -> web.Application:
    app = web.Application()
    handler = ProgressionHandler()
    await init_workers(app, handler.queue, handler.task_list, 2)
    init_routes(app, handler)
    
    return app

def main():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app)

if __name__ == "__main__":
    main()