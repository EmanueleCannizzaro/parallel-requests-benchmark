import aiohttp
import asyncio
import logging
import os

from config import config, logger
from timer import timer


logger = logging.getLogger('parallel_requests_benchmark.test_async_aiohttp_asyncio')


async def fetch(session, url, logger):
    try:
        response = await session.get(url)
        response.raise_for_status()
        json_response = await response.json()
        logger.info(json_response['uuid'])
    except aiohttp.ClientConnectionError:
        logger.error("There was a connection error.")
    except aiohttp.ClientResponseError as http_err:
        logger.error(f"HTTP error occurred: {http_err.status} - {http_err.message}")
    except aiohttp.ClientPayloadError:
        logger.error("There was an error with the response payload.")
    except asyncio.TimeoutError:
        logger.error("The request timed out.")
    except aiohttp.ClientError as err:
        logger.error(f"An error occurred: {err}")

async def main_async():
    no_of_executed_tasks : int = 0
    results = []
    try:
        timeout = aiohttp.ClientTimeout(total=config.TIMEOUT) 
        connector = aiohttp.TCPConnector(limit=config.MAX_CONNECTIONS, 
                                         limit_per_host=config.MAX_KEEPALIVE_CONNECTIONS)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            for batch_start in range(0, config.NO_OF_TASKS, config.NO_OF_TASKS_IN_BATCH):
                batch_end = min(batch_start + config.NO_OF_TASKS_IN_BATCH, config.NO_OF_TASKS)
                tasks = [fetch(session, config.URL, task_id, logger) for task_id in range(batch_start, batch_end)]
                _results = await asyncio.gather(*tasks, return_exceptions=True)
                if (batch_start > 0) and (batch_end < config.NO_OF_TASKS):
                    await asyncio.sleep(config.INTERVAL_BETWEEN_BATCHES)
                no_of_executed_tasks += len(tasks)
                results.extend(_results)
            return results
    except Exception as e:
        logger.warning(f":::ERROR::: Not all the tasks have been completed! \nError: {e}")

    if no_of_executed_tasks != config.NO_OF_TASKS:
        logger.warning(f":::WARNING::: Only {no_of_executed_tasks} out of {config.NO_OF_TASKS} tasks have been completed.")



@timer(name=os.path.splitext(os.path.basename(__file__))[0], number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    asyncio.run(main_async())


if __name__ == '__main__':
    main()