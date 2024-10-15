from concurrent.futures import ThreadPoolExecutor
import requests
import logging

from config import config, logger
from timer import timer
from test_synchronous import fetch


logger = logging.getLogger('parallel_requests_benchmark.test_multithreading')


@timer(number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    with ThreadPoolExecutor(max_workers=config.NO_OF_TASKS) as executor:
        with requests.Session() as session:
            executor.map(fetch, [session] * config.NO_OF_TASKS, [config.URL] * config.NO_OF_TASKS)
            executor.shutdown(wait=True)


if __name__ == '__main__':
    main()