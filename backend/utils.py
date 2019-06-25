import asyncio
import multiprocessing
from concurrent.futures.process import ProcessPoolExecutor
import signal

from aiohttp import web


def warm() -> None:
    # should be executed only in child processes
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def clean()-> None:
    # should be executed only in child processes
    signal.signal(signal.SIGINT, signal.SIG_DFL)

async def setup_executor(app: web.Application):

    num_of_workers = multiprocessing.cpu_count()

    # our tasks are cpu-bound so we choose ProcessPoolExecutor
    executor =  ProcessPoolExecutor(max_workers=num_of_workers)
    loop = asyncio.get_event_loop()
    run = loop.run_in_executor

    fs = [run(executor, warm) for i in range(0, num_of_workers)]
    await asyncio.gather(*fs)

    async def close_executor() -> None:
        fs = [run(executor, clean) for i in range(0, num_of_workers)]
        await asyncio.shield(asyncio.gather(*fs))
        executor.shutdown(wait=True)

    return (executor, close_executor)
