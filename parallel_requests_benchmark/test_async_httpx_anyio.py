import anyio
import httpx
import logging
import os

from config import config, logger
from timer import timer
from test_async_httpx_asyncio import fetch

logger = logging.getLogger('parallel_requests_benchmark.test_async_httpx_anyio')


async def main_async():
    no_of_executed_tasks : int = 0
    results = []
    try:
        limits = httpx.Limits(max_connections=config.MAX_CONNECTIONS, 
                              max_keepalive_connections=config.MAX_KEEPALIVE_CONNECTIONS)
        async with httpx.AsyncClient(timeout=config.TIMEOUT, limits=limits) as client:
            for batch_start in range(0, config.NO_OF_TASKS, config.NO_OF_TASKS_IN_BATCH):
                batch_end = min(batch_start + config.NO_OF_TASKS_IN_BATCH, config.NO_OF_TASKS)
                async with anyio.create_task_group() as tg:
                    tasks = [tg.start_soon(fetch, client, config.URL, task_id, logger) for task_id in range(batch_start, batch_end)]
                    #results = 
                if (batch_start > 0) and (batch_end < config.NO_OF_TASKS):
                    await anyio.sleep(config.INTERVAL_BETWEEN_BATCHES)
                _results = tasks
                no_of_executed_tasks += len(tasks)
                results.extend(_results)
            return results
    except Exception as e:
        logger.warning(f":::ERROR::: Not all the tasks have been completed! \nError: {e}")

    if no_of_executed_tasks != config.NO_OF_TASKS:
        logger.warning(f":::WARNING::: Only {no_of_executed_tasks} out of {config.NO_OF_TASKS} tasks have been completed.")


@timer(name=os.path.splitext(os.path.basename(__file__))[0], number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    anyio.run(main_async)

if __name__ == '__main__':
    main()