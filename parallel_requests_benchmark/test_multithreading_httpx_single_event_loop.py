import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import httpx
import logging
import os

from config import config, logger
from timer import timer
from test_async_httpx_asyncio import fetch


logger = logging.getLogger('parallel_requests_benchmark.test_multithreading_httpx_single_event_loop')


@timer(name=os.path.splitext(os.path.basename(__file__))[0], 
       number=config.NO_OF_NUMBERS, 
       repeat=config.NO_OF_REPEATS)
def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks_per_thread = config.NO_OF_TASKS // config.NO_OF_THREADS

    async def run_requests(task_count):
        async with httpx.AsyncClient() as client:
            tasks = [fetch(client, config.URL, task_id, logger) for task_id in range(task_count)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Request failed: {result}")
                else:
                    logger.info(f"Request completed successfully: {result}")

    def create_and_run_event_loop(task_count, loop):
        try:
            loop.run_until_complete(run_requests(task_count))
        except Exception as e:
            logger.error(f"Error in event loop: {e}")
        finally:
            loop.close()

    with ThreadPoolExecutor(max_workers=config.NO_OF_THREADS) as executor:
        futures = [executor.submit(create_and_run_event_loop, tasks_per_thread, loop) for _ in range(config.NO_OF_THREADS)]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error in thread execution: {e}")


if __name__ == '__main__':
    main()