import anyio
import httpx
import logging

from config import config, logger
from timer import timer


logger = logging.getLogger('parallel_requests_benchmark.test_async_httpx_anyio')


async def fetch(client, url):
    try:
        response = await client.get(url)
        json_response = response.json()
        logger.debug(json_response['uuid'])
        await anyio.sleep(config.MINIMUM_WAITING_TIME)
    except httpx.TimeoutException:
        print("The request timed out.")
    except httpx.ConnectError:
        print("There was a connection error.")
    except httpx.HTTPStatusError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except httpx.RequestError as req_err:
        print(f"An error occurred: {req_err}")


async def main_async():
    try:
        async with httpx.AsyncClient(timeout=config.TIMEOUT) as client:
            no_of_executed_tasks : int = 0
            for batch_start in range(0, config.NO_OF_TASKS, config.NO_TASKS_IN_BATCH):
                batch_end = min(batch_start + config.NO_TASKS_IN_BATCH, config.NO_OF_TASKS)
                async with anyio.create_task_group() as tg:
                    tasks = [tg.start_soon(fetch, client, config.URL) for _ in range(batch_start, batch_end)]
                if (batch_start > 0) and (batch_end < config.NO_OF_TASKS):
                    await anyio.sleep(config.INTERVAL_BETWEEN_BATCHES)
                no_of_executed_tasks += batch_end - batch_start
    except:
        if no_of_executed_tasks != config.NO_OF_TASKS:
            logger.warning(f":::WARNING::: Not all the tasks have been completed!")
    assert(no_of_executed_tasks == config.NO_OF_TASKS)


@timer(number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    anyio.run(main_async)

if __name__ == '__main__':
    main()