import json
import asyncio
import enum
from aiohttp import web


class Status(enum.Enum):
    QUEUED = 1
    RUNNING = 2


# In 3.7 there could be a dataclass wrapper
class Task:
    def __init__(self,
                index: int,
                count: int,
                delta: float,
                start: float,
                interval: float,
                current_value: float = 0,
                status: Status = Status.QUEUED):
        self.index = index
        self.count = count
        self.delta = delta
        self.start = start
        self.interval = interval
        self.current_value = current_value
        self.status = status
        self.start_time = -1
   
    def toJSON(self):
        # Basic JSON class representation 
        data = self.__dict__
        data["status"] = "Running" if data["status"] == Status.RUNNING else "Queued"

        return data


class ProgressionHandler:
    def __init__(self) -> None:
        self.queue = asyncio.Queue(loop=asyncio.get_event_loop())
        # I think it is not a best way to solve view request, but right now
        # I can't find another
        self.task_list = list()
        self._index = 0

    async def index(self, request: web.Request) -> web.Response:
        return web.Response(status=200,
                            body=json.dumps([i.toJSON() for i in self.task_list]),
                            content_type='application/json')

    async def add_task(self, request: web.Request) -> web.Response:
        post_data = await request.json()

        task = Task(index=self._index,
                    count=post_data["count"],
                    delta=post_data["delta"],
                    start=post_data["start"],
                    interval=post_data["interval"])
        self._index += 1

        self.task_list.append(task)

        await self.queue.put(task)

        return web.Response(status=200, text="Success")
