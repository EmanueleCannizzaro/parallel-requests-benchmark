import logging
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from config import config, logger
from timer import timer


logger = logging.getLogger('parallel_requests_benchmark.test_synchronous_requests')


def fetch(session, url, task_id, logger):
    try:
        with session.get(url, timeout=config.TIMEOUT) as response:
            logger.info(response.json()['uuid'])
            return task_id
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.ConnectionError:
        print("There was a connection error.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")


@timer(name=os.path.splitext(os.path.basename(__file__))[0], number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    with requests.Session() as session:
        retry_strategy = Retry(
            total=config.RETRIES,
            backoff_factor=config.BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        for _ in range(config.NO_OF_TASKS):
            fetch(session, config.URL, 0, logger)


if __name__ == '__main__':
    main()