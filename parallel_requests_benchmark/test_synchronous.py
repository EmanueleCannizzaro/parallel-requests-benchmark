import logging
import requests

from config import config, logger
from timer import timer


logger = logging.getLogger('parallel_requests_benchmark.test_synchronous')


def fetch(session, url):
    try:
        with session.get(url, timeout=config.TIMEOUT) as response:
            logger.debug(response.json()['uuid'])
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.ConnectionError:
        print("There was a connection error.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")


@timer(number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    with requests.Session() as session:
        for _ in range(config.NO_OF_TASKS):
            fetch(session, config.URL)


if __name__ == '__main__':
    main()