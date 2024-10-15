import httpx
import logging

from config import config, logger
from timer import timer
from test_synchronous import fetch


logger = logging.getLogger('parallel_requests_benchmark.test_synchronou_httpx')


def fetch(client, url):
    with client.get(url, timeout=config.TIMEOUT) as response:
        try:
            logger.debug(response.json()['uuid'])
        except httpx.TimeoutException:
            print("The request timed out.")
        except httpx.ConnectError:
            print("There was a connection error.")
        except httpx.HTTPStatusError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except httpx.RequestError as req_err:
            print(f"An error occurred: {req_err}")


@timer(number=config.NO_OF_NUMBERS, repeat=config.NO_OF_REPEATS)
def main():
    with httpx.Client() as client:
        for _ in range(config.NO_OF_TASKS):
            fetch(client, config.URL)


if __name__ == '__main__':
    main()