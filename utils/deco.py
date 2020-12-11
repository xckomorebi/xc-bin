import time
from functools import wraps

def timed(func):
    @wraps(func)
    def wrap(*arg, **kwargs):
        t = time.time()
        ret = func(*arg, **kwargs)
        print(f"Runtime for '{func.__name__}' is {time.time()-t} seconds")

        return ret

    return wrap

def retry(max_trials = 5, wait_time = 3, traceback = False):
    if not 'logger' in vars():
        import logging
        logging.basicConfig(filename='retry.log', filemode='a',
                    level=logging.INFO, format = '%(asctime)s - %(levelname)s: %(message)s',\
                     datefmt = '%m/%d/%Y %H:%M:%S')
        logger = logging.getLogger(__name__)
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(max_trials):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if traceback:
                        logger.error(f'trial {_}: {func.__name__} failed, retry in {wait_time} seconds.', exc_info=e)
                    else: 
                        logger.error(f'trial {_}: {func.__name__} failed, retry in {wait_time} seconds. {e}')
                    time.sleep(wait_time)
            logger.error(f'{func.__name__} failed after {max_trials} trials')

        return wrapper
    
    return deco