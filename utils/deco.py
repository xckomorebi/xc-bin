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

def write_into_log(func):
    raise NotImplementedError

