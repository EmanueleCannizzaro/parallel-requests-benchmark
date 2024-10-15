import asyncio
import httpx
import logging

from config import config, logger
from timer import timer
from test_async_aiohttp_asyncio import fetch


logger = logging.getLogger('parallel_requests_benchmark.test_async_httpx_asyncio')


async def main_async():
    try:
        async with httpx.AsyncClient(timeout=config.TIMEOUT) as client:
            no_of_executed_tasks : int = 0
            for batch_start in range(0, config.NO_OF_TASKS, config.NO_TASKS_IN_BATCH):
                batch_end = min(batch_start + config.NO_TASKS_IN_BATCH, config.NO_OF_TASKS)
                tasks = [fetch(client, config.URL) for _ in range(batch_start, batch_end)]
                await asyncio.gather(*tasks)
                if (batch_start > 0) and (batch_end < config.NO_OF_TASKS):
                    await asyncio.sleep(config.INTERVAL_BETWEEN_BATCHES)
                no_of_executed_tasks += batch_end - batch_start
    except:
        if no_of_executed_tasks != config.NO_OF_TASKS:
            logger.warning(f":::WARNING::: Not all the tasks have been completed!")
    assert(no_of_executed_tasks == config.NO_OF_TASKS)


@timer(number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    asyncio.run(main_async())

if __name__ == '__main__':
    main()