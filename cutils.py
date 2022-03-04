from collections.abc import Iterable, Sequence
import math

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

def find_last_index(x: Sequence, target):
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

def get_factors(n):
    factors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(int(n // i))

    return factors

def ordered_unique(lst):
    return list(dict.fromkeys(lst))