# Imports

from collections import namedtuple
from collections.abc import Iterable, Sequence
import math
import statistics
import time
from typing import Callable

# Functions

def contains(x: Iterable, elements: Iterable) -> bool:
    return any(elem in x for elem in elements)

def chunk_list(lst: list, n: int) -> list:
    """Splits a list into n sized chunks

    Args:
        lst (list): a list
        n (int): number of items in chunk

    Yields:
        list: A list of lists of size n, with last list
        being of size len(lst) mod n | n
    """
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def display_time(seconds: float):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return f"{h} hours, {m} minutes, and {s:.2f} seconds"

def even_split(lst: list, n: int) -> list[list]:
    """Breaks a list into n roughly equal parts

    Args:
        lst (list): List to split
        n (int): Number of parts

    Returns:
        list: List of n lists
    """
    if n <= 0:
        raise ValueError("n must be greater than 0")
        
    k, m = divmod(len(lst), n)

    return [lst[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)]

def find_last_index(x: Sequence, target) -> any:
    for i in range(len(x) - 1, -1, -1):
        if x[i] == target:
            return i

    return None

def flatten(container: Iterable) -> list:
    """Flatten an arbitrarily nested list. Does
    not unpack string values. Converting a generator
    object to a list is faster than .append.

    Args:
        container (Iterable): Any container

    Returns:
        list: A flattened list
    """
    def _flatten(container: Iterable):
        for i in container:
            if isinstance(i, (list, set, tuple)):
                for j in _flatten(i):
                    yield j
            else:
                yield i

    return list(_flatten(container))

def get_factors(n: int) -> set:
    if isinstance(n, int) is False:
        raise(ValueError("Must pass in an integer"))

    factors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(int(n // i))

    return factors

def ordered_unique(lst: list) -> list:
    return list(dict.fromkeys(lst))

def _time_func(func: Callable) -> float:
    start = time.perf_counter()
    func()
    elapsed = time.perf_counter() - start
    
    return elapsed

def time_func(
    func: Callable, 
    iterations: int=1,
    warmups: int=0,
    quiet: bool=False
) -> tuple[float, float]:
    """Pass in a function to be timed, along with how many times it
    should be run, ex:
        cutils.time_func(lambda: time.sleep(1), 100)
    will run time.sleep(1) 100 times.

    Args:
        func (Callable): Any function
        iterations (int, optional): Number of times to run func. Defaults to 1.
        quiet (bool, optional): Whether to print stats. Defaults to False.

    Returns:
        tuple[float, float]: (total time, average time)
    """
    for _ in range(warmups):
        func()

    times = [_time_func(func) for _ in range(iterations)]
    total = sum(times)
    avg_elapsed = total / iterations
    min_elapsed = min(times)
    max_elapsed = max(times)
    sd_elapsed = statistics.stdev(times)

    if avg_elapsed < 0.1:
        avg_display = f"{avg_elapsed * 1_000_000:.3f} microseconds"
    else:
        avg_display = f"{avg_elapsed:.2f} seconds"

    if quiet is False:
        result = (
            f"Function ran {iterations:,} times and completed in {display_time(total)} "
            f"for an average time of {avg_display}"
        )

        print(result)

    Tup = namedtuple("times", ["avg", "min", "max", "sd", "total", "raw_times"])
    res = Tup(
        avg=avg_elapsed,
        min=min_elapsed,
        max=max_elapsed,
        sd=sd_elapsed,
        total=total,
        raw_times=times
    )

    return res
