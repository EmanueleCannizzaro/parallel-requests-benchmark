import inspect
import logging
import os
# from rich import print
import timeit

from config import config, logger


logger = logging.getLogger('parallel_requests_benchmark.timer')


def timer(number, repeat, name=''):
    def wrapper(func):
        def inner(*args, **kwargs):
            # Determine the function name if not provided
            actual_name = name or os.path.splitext(os.path.basename(inspect.getfile(func)))[0]
            # print(f"Now executing '{actual_name}'...")            
            # Measure the execution time
            runs = timeit.repeat(func, number=number, repeat=repeat)
            average_runtime : float = sum(runs) / len(runs)
            average_single_runtime : float = sum(runs) / len(runs) / config.NO_OF_TASKS
            message = "The execution time for a single run and the total runs of \033[32m{name:^48}\033[0m are \033[32m{average_single_runtime:>20.6f}\033[0m and \033[32m{average_runtime:>20.6f}\033[0m."
            message_formatted = message.format(**{'name': name, 'average_runtime': average_runtime, 'average_single_runtime': average_single_runtime})
            logger.debug(message_formatted)
            print(message_formatted)
            return runs
        return inner
    return wrapper
