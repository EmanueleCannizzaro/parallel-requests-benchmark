import asyncio
import httpx
import logging
import os

from config import config, logger
from timer import timer



logger = logging.getLogger('parallel_requests_benchmark.test_async_httpx_asyncio')


async def fetch(client, url, logger):
    try:
        response = await client.get(url)
        response.raise_for_status()
        json_response = response.json()
        logger.info(json_response['uuid'])
    except httpx.ConnectError:
        logger.error("There was a connection error.")
    except httpx.HTTPStatusError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except httpx.TimeoutException:
        logger.error("The request timed out.")
    except httpx.RequestError as req_err:
        logger.error(f"An error occurred: {req_err}")


async def main_async():
    no_of_executed_tasks : int = 0
    try:
        async with httpx.AsyncClient(timeout=config.TIMEOUT) as client:
            for batch_start in range(0, config.NO_OF_TASKS, config.NO_TASKS_IN_BATCH):
                batch_end = min(batch_start + config.NO_TASKS_IN_BATCH, config.NO_OF_TASKS)
                tasks = [fetch(client, config.URL, logger) for _ in range(batch_start, batch_end)]
                await asyncio.gather(*tasks, return_exceptions=True)
                if (batch_start > 0) and (batch_end < config.NO_OF_TASKS):
                    await asyncio.sleep(config.INTERVAL_BETWEEN_BATCHES)
                no_of_executed_tasks += batch_end - batch_start
    except Exception as e:
        logger.warning(f":::ERROR::: Not all the tasks have been completed! \nError: {e}")

    if no_of_executed_tasks != config.NO_OF_TASKS:
        logger.warning(f":::WARNING::: Only {no_of_executed_tasks} out of {config.NO_OF_TASKS} tasks have been completed.")


@timer(name=os.path.splitext(os.path.basename(__file__))[0], number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    asyncio.run(main_async())

if __name__ == '__main__':
    main()