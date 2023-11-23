import time
import sys
from loguru import logger

logger.add(sys.stderr, level="ERROR")


def calc_async_time(func):
    async def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = await func(*args, **kwargs)
        end_time = time.monotonic()
        logger.debug(f"Coroutine {func.__name__} took {(end_time - start_time) *1000} seconds to complete.")
        return result

    return wrapper
