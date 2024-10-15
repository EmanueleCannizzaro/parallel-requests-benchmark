import logging
from functools import wraps

def mylogger(logger_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(logger_name)
            return func(logger, *args, **kwargs)
        return wrapper
    return decorator

# Example usage
@mylogger("my_custom_logger")
def example_function(logger, message):
    logger.info(message)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    example_function("Hello, this is a log message!")
