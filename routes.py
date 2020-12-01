from views import ProgressionHandler
from aiohttp import web


def init_routes(app: web.Application, handler: ProgressionHandler) -> None:
    add_route = app.router.add_route

    add_route('GET', '/', handler.index, name='index')
    add_route('POST', '/add_task', handler.add_task, name='add_task')
