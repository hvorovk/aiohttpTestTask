import argparse
import asyncio
import os
import pathlib
import time
from aiohttp import web
from contextlib import suppress

from views import Task, Status


async def worker(queue: asyncio.Queue, task_list: list, name: str):
    print(f'{name} is up');
    
    while True:
        task: Task = await queue.get()
        print(f'{name} got the task {task.index}')
        task.current_value = task.start
        task.status = Status.RUNNING
        task.start_time = int(time.time())

        for _ in range(task.count):
            task.current_value += task.delta
            await asyncio.sleep(task.interval)

        task_list.remove(task)
        print(f'{name} finished the task {task.index}')


async def init_workers(app: web.Application, queue: asyncio.Queue, task_list: list,  max_workers: int = 10, ):
    workers_list: list = []

    for i in range(max_workers):
        workers_list.append(asyncio.create_task(worker(queue, task_list, f'Worker {i+1}')))

    async def close_workers(app: web.Application) -> None:
        for worker in workers_list:
            worker.cancel()
            with suppress(asyncio.CancelledError):
                await worker

    app.on_cleanup.append(close_workers)