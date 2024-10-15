from multiprocessing.pool import Pool
import requests
import logging

from config import config, logger
from timer import timer
from test_synchronous import fetch


logger = logging.getLogger('parallel_requests_benchmark.test_multiprocessing')


@timer(number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    with Pool() as pool:
        with requests.Session() as session:
            pool.starmap(fetch, [(session, config.URL) for _ in range(config.NO_OF_TASKS)])


if __name__ == '__main__':
    main()