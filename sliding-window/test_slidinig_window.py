from functools import wraps
from typing import Callable
from sliding_window import SlidingWindowRateLimiter
import logging

logger = logging.getLogger(__name__)

class RateLimitExceeded(Exception):
    pass

def rate_limit(
    rate_limiter: SlidingWindowRateLimiter,
    client_id_func: Callable = lambda: "default"
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            client_id = client_id_func()
            if not rate_limiter.is_allowed(client_id):
                reset_time = rate_limiter.get_time_to_reset(client_id=client_id)
                raise RateLimitExceeded(
                    f"Rate limit exceeded. Try again in {reset_time} seconds."
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

def test_rate_limit():
    rate_limiter = SlidingWindowRateLimiter(max_requests=10, window_size=10)
    @rate_limit(rate_limiter)
    def my_function():
        print("Function executed")

    try:
        for _ in range(15):
            my_function()
    except RateLimitExceeded as e:
        print(e)
    import time
    time.sleep(10)
    try:
        for _ in range(15):
            my_function()
    except RateLimitExceeded as e:
        print(e)

if __name__ == "__main__":
    test_rate_limit()