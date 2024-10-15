import logging

class Config():
    NO_OF_TASKS : int = 5
    NO_TASKS_IN_BATCH : int = 100
    URL : str = 'https://httpbin.org/uuid'
    TIMEOUT : float = 15.0
    INTERVAL_BETWEEN_BATCHES : float = 3.0
    # MINIMUM_WAITING_TIME : float =0.001
    RETRIES : int = 1
    BACKOFF_FACTOR : float = 0.3

    '''
    The timeit.repeat function in Python is used to measure the execution time of code repeatedly. Here are the key options:

        stmt (default: 'pass'): The code statement to be executed. 
            It can be a string or callable function. 
        setup (default: 'pass'): The setup code that runs before executing stmt. 
            It's executed once initially to set up any preconditions for the measured code. 
            Typically used for imports or initializing variables.
        timer (default: timeit.default_timer): 
            A timer function that provides time measurements. 
            It usually defaults to the most precise clock available on the system.
        number (default: 1000000): The number of times the stmt is executed per repetition. 
            You can set it to control how many times the function should be executed in each iteration.
        repeat (default: 5): The number of times the experiment should be repeated. 
            The return value is a list with the times from each repetition, which helps analyze the variability of execution times.
    '''
    NO_OF_NUMBERS : int = 1
    NO_OF_REPEATS : int = 1


logger = logging.getLogger('parallel_requests_benchmark')
logging.basicConfig(filename='parallel_requests_benchmark.log', 
                    encoding='utf-8', 
                    level=logging.INFO)
logger.info('\n\nThis is a new execution of the program.\n\n')

config = Config()
