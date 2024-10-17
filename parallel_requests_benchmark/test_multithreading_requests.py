from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time

from config import config, logger
from timer import timer
from test_synchronous_requests import fetch


logger = logging.getLogger('parallel_requests_benchmark.test_multithreading_requests')


@timer(name=os.path.splitext(os.path.basename(__file__))[0], 
       number=config.NO_OF_NUMBERS, 
       repeat=config.NO_OF_REPEATS)
def main():
    with ThreadPoolExecutor(max_workers=config.NO_OF_TASKS_IN_BATCH) as executor:
        with requests.Session() as session:
            retries = Retry(
                total=config.RETRIES,
                backoff_factor=config.BACKOFF_FACTOR,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            adapter = HTTPAdapter(pool_connections=config.POOL_CONNECTIONS, 
                                  pool_maxsize=config.POOL_MAXSIZE, max_retries=retries)
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            # executor.map(fetch, [session] * config.NO_OF_TASKS, 
            #              [config.URL] * config.NO_OF_TASKS, 
            #              range(config.NO_OF_TASKS), 
            #              [logger] * config.NO_OF_TASKS)
            # executor.shutdown(wait=True)
            # Use executor to submit fetch function and track futures for better control
            futures = [executor.submit(fetch, session, config.URL, task_id, logger) for task_id in range(config.NO_OF_TASKS)]
            for future in as_completed(futures):
                try:
                    result = future.result()
                    logger.info(f"Request completed successfully: {result}")
                except requests.exceptions.RequestException as e:
                    logger.error(f"Request failed: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")
                # finally:
                #     time.sleep(config.MINIMUM_WAITING_TIME)


if __name__ == '__main__':
    main()