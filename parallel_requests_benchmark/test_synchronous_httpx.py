import httpx
import logging
import os

from config import config, logger
from timer import timer
from test_synchronous_requests import fetch


logger = logging.getLogger('parallel_requests_benchmark.test_synchronous_httpx')


def fetch(client, url, logger):
    try:
        response = client.get(url)
        logger.info(response.json()['uuid'])
    except httpx.TimeoutException:
        print("The request timed out.")
    except httpx.ConnectError:
        print("There was a connection error.")
    except httpx.HTTPStatusError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except httpx.RequestError as req_err:
        print(f"An error occurred: {req_err}")


@timer(name=os.path.splitext(os.path.basename(__file__))[0], number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    with httpx.Client(timeout=config.TIMEOUT) as client:
        for _ in range(config.NO_OF_TASKS):
            fetch(client, config.URL, logger)


if __name__ == '__main__':
    main()