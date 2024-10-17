from multiprocessing.pool import Pool
import requests
import logging
import os

from config import config, logger
from timer import timer
from test_synchronous_requests import fetch


logger = logging.getLogger('parallel_requests_benchmark.test_multiprocessing_requests')


@timer(name=os.path.splitext(os.path.basename(__file__))[0], number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    with Pool() as pool:
        with requests.Session() as session:
            pool.starmap(fetch, [(session, config.URL, task_id, logger) for task_id in range(config.NO_OF_TASKS)])


if __name__ == '__main__':
    main()