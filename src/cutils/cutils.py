# Imports

import abc
import concurrent.futures
from collections.abc import Callable, Generator, Iterable, MutableMapping, Sequence
from dataclasses import dataclass
import functools
import math
import random
import re
import statistics
import time
import threading
from typing import Any, Literal, Protocol, Union

# Types

Real = Union[int, float]

ParallelOption = Literal["process", "thread"]


class Comparable(Protocol):
    @abc.abstractmethod
    def __lt__(self, other) -> bool:
        pass


@dataclass
class TimeFuncRes:
    avg: Real
    median: Real
    min: Real
    max: Real
    sd: Real
    total: Real
    raw_times: list[Real]


# Functions


def contains(source: Iterable, query: Iterable) -> bool:
    """Test if argument 1 contains any element of
    argument 2.

    Args:
        source (Iterable): arg 1
        query (Iterable): arg 2

    Returns:
        bool: True if arg 1 contains an element of arg 2
    """
    # Note that this method seems to be, on average, faster than using any().
    # any() can be faster in the case that no elements of the query are in the source,
    # but the difference is negligeble. However, in the case that elements of the query
    # are in the source, this method is much faster.
    for i in query:
        if i in source:
            return True

    return False


def _chunk_seq(seq: Sequence, n: int) -> Generator[Sequence, None, None]:
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def chunk_seq(seq: Sequence, n: int) -> list:
    """Splits a list into n sized chunks

    Args:
        seq (Sequence): a Sequence- any indexable object
        n (int): number of items in chunk

    Returns:
        list: A list of sequences of size n, with last sequence
        being of size len(lst) mod n | n
    """
    if n <= 0:
        raise ValueError("chunk size must be a positive integer")

    return list(_chunk_seq(seq, n))


def clamp(num: Comparable, min: Comparable, max: Comparable) -> Comparable:
    if num > max:
        return max
    elif num < min:
        return min
    else:
        return num


def _random_chunk_seq(seq: Sequence, min: int, max: int):
    i = 0
    while i < len(seq):
        chunk_size = random.randint(min, max)
        yield seq[i : i + chunk_size]

        i += chunk_size


def random_chunk_seq(seq: Sequence, min: int, max: int):
    return list(_random_chunk_seq(seq, min, max))


def display_time(seconds: float) -> str:
    """Turns seconds into hours, minutes, seconds

    Args:
        seconds (float): seconds

    Returns:
        str: A string of hours, minutes, seconds
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return f"{h} hours, {m} minutes, and {s:.2f} seconds"


def even_split(seq: Sequence, n: int) -> list:
    """Breaks a list into n roughly equal parts

    Args:
        seq (Sequence): Sequence to split
        n (int): Number of parts

    Returns:
        list: List of n elements of the sequence.
        Pads with empty list if n > len(seqence)
    """
    if n <= 0:
        raise ValueError("n must be an integer greater than 0")

    k, m = divmod(len(seq), n)

    return [seq[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)]


def find_last_index(x: Sequence, target: Any) -> int:
    """Finds the last index that the target occurs at

    Args:
        x (Sequence): the haystack
        target (Any): the needle

    Returns:
        Optional[int]: the last index, or none if it does not exist
    """
    for i in range(len(x) - 1, -1, -1):
        if x[i] == target:
            return i

    raise ValueError("target not found")


def flatten(container: Iterable) -> list:
    """Flatten an arbitrarily nested list. Does
    not unpack string values.

    Args:
        container (Iterable): Any container

    Returns:
        list: A flattened list
    """

    # Converting a generator object to a list is faster than .append.
    def _flatten(container: Iterable):
        for i in container:
            if isinstance(i, (list, set, tuple)):
                for j in _flatten(i):
                    yield j
            else:
                yield i

    return list(_flatten(container))


def _flatten_dict(d: MutableMapping, parent_key: str, sep: str):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, sep=sep).items()
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = "", sep: str = "."):
    return dict(_flatten_dict(d, parent_key, sep))


def get_factors(n: int) -> set[int]:
    """Returns the factors of an integer

    Args:
        n (int): number to factorize

    Returns:
        set[int]: unordered set of all factors
    """
    if isinstance(n, int) is False:
        raise (ValueError("Must pass in an integer"))

    factors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(int(n // i))

    return factors


def ordered_unique(x: Iterable) -> list:
    """Gets the unique elements of an iterable,
    preserves the original order unlike calling
    set()

    Args:
        x (Iterable): any Iterable

    Returns:
        list: a list of unique elements, in original order
    """
    return list(dict.fromkeys(x))


def strip_blanks(string: str) -> str:
    """Remove all whitespace from a string

    Args:
        string (str): A string to strip

    Returns:
        str: A string with no whitespace
    """
    string = re.sub(r"(\s|\u180B|\u200B|\u200C|\u200D|\u2060|\uFEFF)+", "", string)

    return string


def _time_func(func: Callable) -> float:
    start = time.perf_counter()
    func()
    elapsed = time.perf_counter() - start

    return elapsed


def time_func(
    func: Callable,
    func_name: str = "Function",
    iterations: int = 1,
    warmups: int = 0,
    quiet: bool = False,
) -> TimeFuncRes:
    """Pass in a function to be timed, along with how many times it
    should be run, ex:
        cutils.time_func(lambda: time.sleep(1), 100)
    will run time.sleep(1) 100 times.

    Args:
        func (Callable): Any function
        iterations (int, optional): Number of times to run func. Defaults to 1.
        warmups (int, optional): Number of times to run func before timing.
            Defaults to 0.
        quiet (bool, optional): Whether to print stats. Defaults to False.

    Returns:
        TimeFuncRes: (average, min, max, sd, total, list of raw times)
    """
    for _ in range(warmups):
        func()

    times = [_time_func(func) for _ in range(iterations)]
    total = sum(times)
    avg_elapsed = total / iterations
    median_elapsed = statistics.median(times)
    min_elapsed = min(times)
    max_elapsed = max(times)

    # standard deviation requires at least two data points
    try:
        sd_elapsed = statistics.stdev(times)
    except statistics.StatisticsError:
        sd_elapsed = 0

    if avg_elapsed < 0.1:
        avg_display = f"{avg_elapsed * 1_000_000:.3f} microseconds"
    else:
        avg_display = f"{avg_elapsed:.2f} seconds"

    if quiet is False:
        result = (
            f"{func_name} ran {iterations:,} times and completed in"
            f" {display_time(total)} for an average time of {avg_display} per run"
        )

        print(result)

    res = TimeFuncRes(
        avg=avg_elapsed,
        median=median_elapsed,
        min=min_elapsed,
        max=max_elapsed,
        sd=sd_elapsed,
        total=total,
        raw_times=times,
    )

    return res


def rate_limited(limit: int, period: int = 1):
    lock = threading.Lock()
    max_per_second = limit / period
    min_interval = 1.0 / max_per_second

    def decorate(func: Callable):
        last_time_called = time.perf_counter()

        @functools.wraps(func)
        def rate_limited_function(*args, **kwargs):
            lock.acquire()
            nonlocal last_time_called
            try:
                elapsed = time.perf_counter() - last_time_called
                left_to_wait = min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)

                return func(*args, **kwargs)
            finally:
                last_time_called = time.perf_counter()
                lock.release()

        return rate_limited_function

    return decorate


def run_parallel(func: Callable, iterable: Iterable, *args, **kwargs):
    with concurrent.futures.ProcessPoolExecutor(*args, **kwargs) as pool:
        return pool.map(func, iterable)
